from dataclasses import dataclass
from typing import List


@dataclass
class Period:
    name: str
    day_from: int
    day_to: int
    temperature: float
    humidity: float
    sunrise_start: str
    sunrise_stop: str
    sunset_start: str
    sunset_stop: str
    red_spectrum: bool


@dataclass
class Config:
    name: str
    periods: List[Period]
