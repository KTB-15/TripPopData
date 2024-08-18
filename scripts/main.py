from common.logger import get_logger
from common.metadata import CSV_NAME
from database.load import DataSaver
from database.model import SGG
import os
import pandas as pd

logger = get_logger('MAIN')

logger.info(os.getcwd())
data = pd.read_csv(CSV_NAME.sgg)
df = data.iloc[0]
logger.info(df.keys())

SGG_data_saver = DataSaver(
    file_name=CSV_NAME.sgg,
    model_class=SGG,
)

SGG_data_saver.load_csv()
sgg_df = SGG_data_saver.data.iloc[0]

logger.info(sgg_df)