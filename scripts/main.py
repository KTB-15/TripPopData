from common.logger import get_logger
from common.metadata import CSV_NAME
from database.save import DataSaver
from database.model import SGG
from database.format import to_SGG
import os
import pandas as pd

logger = get_logger('MAIN')

data = pd.read_csv(CSV_NAME.sgg)
df = data.iloc[0]
logger.info(df.keys())

SGG_data_saver = DataSaver(
    file_name=CSV_NAME.sgg,
    model_class=SGG,
)

SGG_data_saver.load_csv()
SGG_data_saver.save_all(to_SGG)