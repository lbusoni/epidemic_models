
from datetime import datetime


def dataAtToday():
    now = datetime.now()
    return now.strftime("data at %m/%d/%Y")
