from common.logger import get_logger
from database.conn import Base, insert
from typing import Callable, Union
import pandas as pd

_logger = get_logger('LOAD')


# CSV -> Model 가공 후, DB 저장
class DataSaver:
    def __init__(self, file_name, model_class):
        self.file_name: str = file_name
        self.model_class: Base = model_class
        self.data: Union[pd.DataFrame, None] = None  # Daraframe

    def load_csv(self) -> Union[pd.DataFrame, None]:
        try:
            self.data = pd.read_csv(self.file_name)
            return self.data
        except Exception as e:
            _logger.error(f"CSV {self.file_name} 로드 실패. ERROR: {e}")
            return None

    def save_all(self, callback: Callable) -> bool:
        if self.data is None:
            _logger.error("데이터 없음. CSV 로드 필요.")
        _data = self.data.loc
        for _, row in self.data.iterrows():
            _converted = self.convert(row, callback)
            if not _converted:
                continue
            if not insert(_converted):
                _logger.error(f"DB 저장 실패, DATA:{row}")
                return False
        return True

    # CSV -> Model
    def convert(self, fields: pd.Series, callback: Callable) -> Base:
        try:
            return callback(fields)
        except Exception as e:
            _logger.error(f"CSV -> Model 변환 실패. FIELD: {fields}, ERROR: {e}")

    def print_data(self, start=0, end=10):
        _data = self.data.loc
        for idx in range(start, min(end, len(self.data))):
            _logger.info(_data[idx])


__all__ = [DataSaver]