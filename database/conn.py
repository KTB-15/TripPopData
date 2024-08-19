from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from typing import Union, Any, Generic, TypeVar

from common.logger import get_logger

LOGGER = get_logger('CONN')

_engine = create_engine('postgresql+psycopg2://user:123456@localhost:5432/trippop',
                        pool_size=30, max_overflow=60, pool_timeout=5)
Base = declarative_base()
Base.metadata.create_all(_engine)

Session = sessionmaker(bind=_engine)


def insert(data: Base) -> bool:
    session = Session()
    if not data:
        LOGGER.error("EMPTY DATA")
        session.close()
        return False
    try:
        session.add(data)
        session.commit()
        session.close()
        return True
    except IntegrityError as e:
        LOGGER.error(f"무결성 위반됨: {str(e)}")
        session.rollback()
        session.close()
        return True
    except SQLAlchemyError as e:
        LOGGER.error(f"SQL 에러: {str(e)}")
    except Exception as e:
        LOGGER.error(f"DB 로드 실패: {str(e)}")
    finally:
        session.rollback()
        session.close()
    return False


T = TypeVar('T', bound=Base)


def get_filter(field: str, model_class: T, expected: Any) -> Union[T | None]:
    session = Session()
    if not field:
        LOGGER.warning("필드를 넣어주세요.")
        session.close()
        return None
    try:
        _field = getattr(model_class, field)
    except AttributeError:
        LOGGER.error(f"{model_class.__name__}에 {field}가 없어요.")
        session.close()
        return None
    session.close()
    return session.query(model_class).filter(_field == expected).first()


__all__ = [Base, Session, insert, get_filter]
