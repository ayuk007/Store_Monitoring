import pytz
import csv
import math
from datetime import datetime, timedelta
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.tools.date_and_time import Datetime
from src.database.schemas import Base, StoreStatus, StoreTimezone, Report, BusinessHours, get_engine_session

class ReportGenerator:
    def __init__(self):
        engine = create_engine("sqlite:///store_monitoring.db")
        Session = sessionmaker(bind = engine)
        self.session = Session()
        self.datetime = Datetime()
        
    
    def get_business_hrs(self, store_id: str) -> dict:
        business_hrs = self.session.query(BusinessHours).filter(BusinessHours.store_id == store_id).all()
        if len(business_hrs) == 0:
            business_hrs = {business_day: ("00:00:00", "23:59:59") for business_day in range(0, 7)}
        else:
            business_hrs = {b_hrs.day_of_week: (b_hrs.start_time_local, b_hrs.end_time_local) for b_hrs in business_hrs}

        return business_hrs

    def get_timezone(self, store_id: str) -> str:
        timezone = self.session.query(StoreTimezone).filter(StoreTimezone.store_id == store_id).first()
        timezone = timezone.timezone_str if timezone is not None else "America/Chicago"
        return timezone
    
    def generate_report(self, report_id: str):
        unique_store_id = self.session.query(StoreStatus.store_id).distinct().all()
        current_time_utc = self.session.query(func.max(StoreStatus.timestamp_utc)).scalar()

        one_week_ago = datetime.strptime(current_time_utc, self.datetime.UTC_FORMAT) - timedelta(weeks=1)
        one_week_ago = one_week_ago.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        one_day_ago = datetime.strptime(current_time_utc, self.datetime.UTC_FORMAT) - timedelta(days=1)
        one_hour_ago = datetime.strptime(current_time_utc, self.datetime.UTC_FORMAT) - timedelta(hours=1)

        report = dict()

        for store in unique_store_id:
            # Getting all status data according to store_id
            store_statuses = self.session.query(StoreStatus).filter(
                StoreStatus.store_id == store.store_id,
                StoreStatus.timestamp_utc <= current_time_utc,
                StoreStatus.timestamp_utc >= one_week_ago
            ).order_by(StoreStatus.timestamp_utc).all()

            # Getting timezone and business_hrs according to store_id
            timezone = self.get_timezone(store.store_id)
            business_hrs = self.get_business_hrs(store.store_id)

            # Initializing all variables
            dates_visited = list()
            hour_uptime = hour_downtime = 0
            day_uptime = day_downtime = 0
            week_uptime = week_downtime = 0
            prev_time = None

            for status in store_statuses:
                uptime = downtime = 0
                
                # Status of the store
                store_status = status.status
                # Getting date and time string to be used later
                date_str, time_str, _ = status.timestamp_utc.split()
                # Convert timestamp from utc to local. returns: datetime.object, int
                time_local, week_day = self.datetime.convert_utc_to_local(status.timestamp_utc, timezone)
                
                # Checks for the condition if there's any day missing and if so it'll not be included in calculations
                if week_day not in business_hrs.keys():
                    continue
                else:
                    # Defining start time and end time of business wrt timezone
                    start_time_local = business_hrs[week_day][0]
                    end_time_local = business_hrs[week_day][1]  
                    
                    # Checking if the time is between business hours or not
                    if self.datetime.is_within_business_hours(time_local, start_time_local, end_time_local):
                    
                        # Condition if the date is not visited
                        if date_str not in dates_visited:
                            # Adding dates if it does not extis in the list
                            dates_visited.append(date_str)
                            # Calculating uptime and downtime based on the store status
                            if store_status == "active":
                                uptime = self.datetime.calculate_uptime_downtime(time_local, start_time_local)
                            elif store_status == "inactive":
                                downtime = self.datetime.calculate_uptime_downtime(time_local, start_time_local)
                        else:
                            if store_status == "active":
                                uptime = self.datetime.calculate_uptime_downtime(time_local, prev_time)
                            else:
                                downtime = self.datetime.calculate_uptime_downtime(time_local, prev_time)
                            
                        prev_time = self.datetime.convert_utc_to_local(time_str, timezone, True)
                        
                        if store_statuses.index(status)+1 < len(store_statuses) and \
                        store_statuses[store_statuses.index(status)+1].timestamp_utc.split()[0] != date_str:
                            if store_status == "active":
                                uptime += self.datetime.calculate_uptime_downtime(time_local, prev_time)
                            elif store_status == "inactive":
                                downtime += self.datetime.calculate_uptime_downtime(time_local, prev_time)
                        
                        week_uptime += uptime
                        week_downtime += downtime

                        if datetime.strptime(status.timestamp_utc, "%Y-%m-%d %H:%M:%S.%f UTC") >= one_day_ago \
                        and datetime.strptime(status.timestamp_utc, "%Y-%m-%d %H:%M:%S.%f UTC").day == one_day_ago.day:
                            day_uptime += uptime
                            day_downtime += downtime
                        if datetime.strptime(status.timestamp_utc, "%Y-%m-%d %H:%M:%S.%f UTC") >= one_hour_ago:
                            hour_uptime += uptime
                            hour_downtime += downtime

            report[store.store_id] = {
                "week_uptime": math.floor(week_uptime/60),
                "week_downtime": math.floor(week_downtime/60),
                "day_uptime": math.floor(day_uptime/60),
                "day_downtime": math.floor(day_downtime/60),
                "hour_uptime": hour_uptime,
                "hour_downtime": hour_downtime
            }
            hour_uptime = hour_downtime = 0
            day_uptime = day_downtime = 0
            week_uptime = week_downtime = 0
        self.generate_csv(report, report_id)

    def generate_csv(self, report: dict, report_id: str):
        # Define the CSV file name
        csv_file = f'../../files/{report_id}.csv'

        # Define the header for the CSV file
        header = [
            "store_id", 
            "uptime_last_hour(in minutes)", 
            "uptime_last_day(in hours)", 
            "uptime_last_week(in hours)", 
            "downtime_last_hour(in minutes)", 
            "downtime_last_day(in hours)", 
            "downtime_last_week(in hours)"
        ]

        # Open the CSV file in write mode
        with open(csv_file, 'w', newline='') as file:
            csvwriter = csv.writer(file)

            # Write the header
            csvwriter.writerow(header)

            # Iterate through the report dictionary and write each store's data
            for store_id, data in report.items():
                csvwriter.writerow([
                    store_id,
                    data['hour_uptime'],       # in minutes
                    data['day_uptime'],        # in hours
                    data['week_uptime'],       # in hours
                    data['hour_downtime'],     # in minutes
                    data['day_downtime'],      # in hours
                    data['week_downtime']      # in hours
                ])
        
        report_detail = self.session.query(Report).filter(Report.report_id == report_id).first()
        report.status = "Completed"
        report.completed_at = datetime.utcnow()
        report.file_path = csv_file
        self.session.commit()