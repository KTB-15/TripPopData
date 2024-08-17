from common.logger import get_logger
from common.metadata import CSV_NAME
import os
import pandas as pd

logger = get_logger()

logger.info(os.getcwd())
data = pd.read_csv(CSV_NAME.codea)
logger.info(data.iloc[0])
