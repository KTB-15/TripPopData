from common.logger import get_logger
from database.conn import Base, load
import pandas as pd

_logger = get_logger('LOAD')


# CSV -> Model 가공 후, DB 저장
class DataSaver:
    def __init__(self, file_name, model_class):
        self.file_name: str = file_name
        self.model_class: Base = model_class
        self.data = pd.DataFrame()  # Daraframe

    def load_csv(self):
        try:
            self.data = pd.read_csv(self.file_name)
            return self.data
        except Exception as e:
            _logger.error(f"CSV {self.file_name} LOAD FAILED. ERROR: {e}")
            return None

    def save(self, data: Base) -> Base:
        return data if load(data) else None

    # CSV -> Model
    def convert(self, callback) -> Base:
        return callback()


__all__ = [DataSaver]
