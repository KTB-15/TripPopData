from common.logger import get_logger
from common.metadata import CSV_NAME
from database.save import DataSaver
from database.model import SGG, Member
from database.format import to_SGG, to_member
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
member_data_saver = DataSaver(
    file_name=CSV_NAME.traveler,
    model_class=Member
)

# SGG_data_saver.load_csv()
# SGG_data_saver.save_all(to_SGG)

member_data_saver.load_csv()
member_data_saver.save_all(to_member)