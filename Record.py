from enum import Enum
from datetime import date
from datetime import  time
from pydantic import BaseModel


class Duration(Enum):
    THIRTY_MINUTES = "30 минут"
    ONE_HOUR = "1 час"
    HOUR_AND_HALF = "1.5 часа"
    TWO_HOURS = "2 часа"
    GROUP_CALL = "Групповой созвон"
    NOT_SELECTED = "Не выбрано"


class Difficulty(Enum):
    LIGHT = "Лайт"
    STANDARD = "Стандарт"
    HARD = "Хард"
    NOT_SELECTED = "Не выбрано"


class Record(BaseModel):
    date: date
    time: time
    fullname: str
    duration: Duration
    theme: str
    difficulty: Difficulty
