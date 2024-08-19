from common.logger import get_logger
from common.metadata import CSV_NAME
from database.model import SGG, Member, Place
from database.save import DataSaver
from database.format import to_SGG, to_member, to_place

logger = get_logger('MAIN')


def insert_all_SGG():
    SGG_data_saver = DataSaver(
        file_name=CSV_NAME.sgg,
        model_class=SGG,
    )
    SGG_data_saver.load_csv()
    SGG_data_saver.save_all(to_SGG)


def insert_all_member():
    member_data_saver = DataSaver(
        file_name=CSV_NAME.traveler,
        model_class=Member
    )
    member_data_saver.load_csv()
    member_data_saver.save_all(to_member)


def insert_all_place():
    place_data_saver = DataSaver(
        file_name=CSV_NAME.visit_area_info,
        model_class=Place
    )
    place_data_saver.load_csv()
    place_data_saver.save_all(to_place)


# insert_all_SGG()
# insert_all_member()
insert_all_place()
