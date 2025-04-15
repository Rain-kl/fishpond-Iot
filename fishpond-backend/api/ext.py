import random
import time

from .model import MonitorModel, ControllerModel
import api.available_device as available_device

from core.zdb import zdb

monitor_addr_map = {
    "00:12:4B:00:1E:F9:FC:CA": "温湿度",
    "00:12:4B:00:15:D1:5C:83": "光照度",
    "00:12:4B:00:1F:5F:82:23": "ph",
    "00:12:4B:00:1E:F9:FE:29": "水温"
}

controller_addr_map = {
    "00:12:4B:00:1F:5F:84:8C": "继电器",
    "00:12:4B:00:07:5D:D7:D8": "plusB",
}


def get_monitor_data():
    monitor_list = []
    for monitor in available_device.monitors:
        monitor_data = zdb.search(addr=monitor["addr"])
        value = monitor_data.model_dump()[monitor["position"]]
        status = "offline"
        if int(time.time()) - int(monitor_data.updated) < 20:
            status = "online"

        model = MonitorModel(
            id=monitor['id'],
            name=monitor['name'],
            value=value,
            unit=monitor['unit'],
            type=monitor['type'],
            status=status,
            min=monitor['min'],
            max=monitor['max']
        )
        monitor_list.append(model)
    return monitor_list


def random_monitor_data():
    return [MonitorModel(
        id=monitor['id'],
        name=monitor['name'],
        value=random.uniform(monitor['min'], monitor['max']),
        unit=monitor['unit'],
        type=monitor['type'],
        status=random.choice(['online', 'offline']),
        min=monitor['min'],
        max=monitor['max']
    ) for monitor in available_device.monitors]


def random_controller_data():
    return [ControllerModel(
        id=controller['id'],
        name=controller['name'],
        icon=controller['icon'],
        status=random.choice(['online', 'offline']),
        isOn=random.choice([True, False])
    ) for controller in available_device.controllers]
