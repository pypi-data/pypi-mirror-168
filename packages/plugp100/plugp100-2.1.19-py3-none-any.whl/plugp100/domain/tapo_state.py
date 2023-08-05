import base64
import dataclasses
from typing import Optional, Dict, Any

from plugp100.domain.energy_info import EnergyInfo


@dataclasses.dataclass
class TapoDeviceState:
    device_id: str = property(lambda self: self.state["device_id"])
    mac: str = property(lambda self: self.state["mac"])
    nickname: str = property(lambda self: base64.b64decode(self.state["nickname"]).decode("UTF-8"))
    model: str = property(lambda self: self.state["model"])
    type: str = property(lambda self: self.state["type"])
    device_on: bool = property(lambda self: self.state["device_on"])
    brightness: Optional[int] = property(lambda self: self.state["brightness"] if "brightness" in self.state else None)
    hue: Optional[int] = property(lambda self: self.state["hue"] if "hue" in self.state else None)
    saturation: Optional[int] = property(lambda self: self.state["saturation"] if "saturation" in self.state else None)
    color_temp: Optional[int] = property(lambda self: self.state["color_temp"] if "color_temp" in self.state else None)
    overheated: bool = property(lambda self: self.state["overheated"])
    signal_level: int = property(lambda self: self.state["signal_level"])
    rssi: int = property(lambda self: self.state["rssi"])
    energy_info: EnergyInfo = property(lambda self: self._energy_info)

    def __init__(self, state: Dict[str, Any], energy_info: EnergyInfo):
        self.state = state
        self._energy_info = energy_info

    def get_unmapped_state(self) -> Dict[str, Any]:
        return self.state
