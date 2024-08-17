from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from common.logger import get_logger

LOGGER = get_logger()

_engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()
Base.metadata.create_all(_engine)

session = sessionmaker(bind=_engine)()


def load(data: Base) -> bool:
    try:
        session.add(data)
        session.commit()
        session.close()
        return True
    except IntegrityError as e:
        LOGGER.error(f"무결성 위반됨: {str(e)}")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQL 에러: {str(e)}")
    except Exception as e:
        LOGGER.error(f"DB 로드 실패: {str(e)}")
    finally:
        session.rollback()
        session.close()
    return False


__all__ = [Base, session]
