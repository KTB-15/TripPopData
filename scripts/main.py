from common.logger import get_logger
from common.metadata import CSV_NAME_V2, CSV_NAME
from database.model import Member, Place, Visit, SGG
from database.save import DataSaver
from database.format import to_SGG, to_visit, to_place, to_member
from scripts.check import check_type, check_visit_area_type

logger = get_logger('MAIN')


def insert_all_data(file_name: str, model_class, convert):
    logger.info(file_name)
    data_saver = DataSaver(
        file_name=file_name,
        model_class=model_class
    )
    data_saver.load_csv()
    data_saver.save_all(convert)


def insert_all_csv(file_name: str, model_class, convert):
    files = [getattr(CSV_NAME_V2, folder) for folder in 'abcd']
    logger.info(files)
    for file in files:
        data_saver = DataSaver(
            file_name=getattr(file, file_name),
            model_class=model_class
        )
        logger.info(data_saver)
        data_saver.load_csv()
        data_saver.save_all(convert)


# check_visit_area_type(8)

# SGG
insert_all_data(CSV_NAME.sgg, SGG, to_SGG)

# Member
# insert_all_data(CSV_NAME.traveler, Member, to_member)

# All members
insert_all_csv('traveler', Member, to_member)

# Place
# insert_all_data(CSV_NAME.visit_area_info, Place, to_place)

# All places
insert_all_csv('visit_area_info', Place, to_place)

# Visit
# insert_all_data(CSV_NAME.visit_area_info, Visit, to_visit)

# All visits
insert_all_csv('visit_area_info', Visit, to_visit)