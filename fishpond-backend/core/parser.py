import json
import time

from loguru import logger
from .model import ZXDataModel, ZXResponseModel
from .zdb import zx_db


def parse_zx_data_json(zx_data_str: str):
    """
    :param zx_data_str: {A0=0,A4=28.3,A5=23.0,A6=343.3,A7=12.9}
    :return: {"A0":0,"A4":28.3,"A5":23.0,"A6":343.3,"A7":12.9}
    """
    zx_data_str = zx_data_str.replace("{", "").replace("}", "")
    zx_data_list = zx_data_str.split(",")
    zx_data_dict = {}
    for item in zx_data_list:
        key, value = item.split("=")
        zx_data_dict[key] = value
    return zx_data_dict


def parse_zx_response(zx_response_str: str):
    """
    Parse the ZX response string into a ZXResponseModel object.
    """
    zx_response_json = json.loads(zx_response_str)
    print(zx_response_json["data"])
    zx_data_json = parse_zx_data_json(zx_response_json["data"])
    print(zx_response_json)
    zx_data = ZXDataModel(updated=str(int(time.time())), **zx_data_json)
    print(zx_data)
    zx_response = ZXResponseModel(
        method=zx_response_json["method"],
        addr=zx_response_json["addr"],
        data=zx_data
    )
    zx_db.update(zx_response.addr, zx_data)
    logger.debug(f"updated {zx_response.addr}")
