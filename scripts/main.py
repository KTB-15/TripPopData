from common.logger import get_logger
from common.metadata import *
from database.model import *
from database.save import DataSaver
from database.format import *

logger = get_logger('MAIN')


def insert_all_data(file_name: str, model_class, convert):
    data_saver = DataSaver(
        file_name=file_name,
        model_class=model_class
    )
    data_saver.load_csv()
    data_saver.save_all(convert)


def insert_all_csv(file_name: str, model_class, convert):
    files = [CSV_NAME_V2.a[file_name], CSV_NAME_V2.b[file_name], CSV_NAME_V2.c[file_name], CSV_NAME_V2.d[file_name]]
    for file in files:
        data_saver = DataSaver(
            file_name=file,
            model_class=model_class
        )
        data_saver.load_csv()
        data_saver.save_all(convert)

# SGG
# insert_all_data(CSV_NAME.sgg, SGG, to_SGG)

# Member
# insert_all_data(CSV_NAME.traveler, Member, to_member)

# All members
# insert_all_csv(CSV_NAME.traveler, Member, to_member)

# Place
# insert_all_data(CSV_NAME.visit_area_info, Place, to_place)

# All places
# insert_all_csv(CSV_NAME.visit_area_info, Place, to_place)

# Visit
# insert_all_data(CSV_NAME.visit_area_info, Visit, to_visit)

# All visits
# insert_all_csv(CSV_NAME.visit_area_info, Visit, to_visit)
