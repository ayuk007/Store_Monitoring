from datetime import datetime
import pytz
import math

class Datetime:
    def __init__(self):
        self.UTC_FORMAT = '%Y-%m-%d %H:%M:%S.%f UTC'

    def convert_utc_to_local(self, utc_time_str: str, timezone_str: str, is_prevTime: bool = False):

        if is_prevTime:
            utc_time = datetime.strptime(utc_time_str, '%H:%M:%S.%f')
            utc_time = pytz.utc.localize(utc_time)
            local_timezone = pytz.timezone(timezone_str)
            local_time = utc_time.astimezone(local_timezone)
            return local_time.strftime('%H:%M:%S.%f')
            
        utc_time_str = utc_time_str.split(" UTC")[0]
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S.%f')
        utc_time = pytz.utc.localize(utc_time)
        local_timezone = pytz.timezone(timezone_str)
        local_time = utc_time.astimezone(local_timezone)
        
        return datetime.strptime(local_time.strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"), local_time.weekday()

    def parse_time(self, time_str: str):
        # Attempt to parse time with fractional seconds
        try:
            return datetime.strptime(time_str, '%H:%M:%S.%f')
        except ValueError:
            # Fallback to parsing without fractional seconds
            return datetime.strptime(time_str, '%H:%M:%S')

    def parse_date(self, date_str: str):
        # Attempt to parse time with fractional seconds
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f UTC')
        except ValueError:
            # Fallback to parsing without fractional seconds
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S UTC')

    def check_weekday(self, timestamp: str):
        timestamp = datetime.strptime(timestamp, self.UTC_FORMAT)

    def is_within_business_hours(self, timestamp: datetime, start_time_local: str, end_time_local: str) -> bool:
        hour_detail = datetime.strftime(timestamp, "%H:%M:%S")
        return start_time_local <= hour_detail <= end_time_local

    def calculate_uptime_downtime(self, time_local: datetime, diff_from: str):
        time_diff = self.parse_time(datetime.strftime(time_local, "%H:%M:%S.%f")) - self.parse_time(diff_from)
        return abs(math.floor(time_diff.total_seconds()/60))
