import random
from .model import MonitorModel, ControllerModel
import api.available_device as available_device


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
