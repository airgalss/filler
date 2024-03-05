from ..convert import target
from logger import log
from datetime import datetime, timedelta

@target("citizen1")
def convert(data_dict):
    return data_dict