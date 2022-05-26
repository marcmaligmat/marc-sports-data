from datetime import datetime
import pytz


class Date:
    def get_US_date() -> int:
        date = datetime.now(pytz.timezone("US/Central"))
        return int(date.strftime("%Y%m%d"))
