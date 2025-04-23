from .available_monitor import monitors
from .available_controller import controllers

__all__ = ["monitors", "controllers"]

monitor_addr_map = {
    "00:12:4B:00:1E:F9:FC:CA": "温湿度",
    "00:12:4B:00:15:D1:5C:83": "光照度",
    "00:12:4B:00:1F:5F:82:23": "ph",
    "00:12:4B:00:1E:F9:FE:29": "水温",
}

controller_addr_map = {
    "00:12:4B:00:1F:5F:84:8C": "继电器",
    "00:12:4B:00:07:5D:D7:D8": "plusB",
}
