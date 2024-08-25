import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine

Base = declarative_base()

class StoreStatus(Base):
    """
    Schema for status of all the stores based on the polls.
    
    id: unique record id.
    store_id : unique_id provided to the store.
    status : status of the store as active or inactive.
    timestamp_utc: time of the response to the poll.
    """
    __tablename__ = 'store_status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column("store_id", Integer, nullable = False)
    status = Column("status", String, nullable = False)
    timestamp_utc = Column("timestamp_utc", String, nullable = False)

class BusinessHours(Base):
    """
    Schema for business hours of the all stores
    
    id: unique record id.
    store_id : unique_id provided to the store.
    day_of_week : refers to the day of the week. 0: Monday  6: Sunday.
    start_time_local : starting time of the store as local time zone.
    end_time_local : closing time of the store as local time zone.
    """
    __tablename__ = 'business_hours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column("store_id", Integer, nullable = False)
    day_of_week = Column("day_of_week", Integer, nullable = False)
    start_time_local = Column("start_time_local", String, nullable = False)
    end_time_local = Column("end_time_local", String, nullable = False)

class StoreTimezone(Base):
    """
    Schema for store timezone information.

    id : unique id for the records.
    store_id : unique id for each store.
    timezone_str : timezone string according to the local timezone of store.
    """
    __tablename__ = "store_timezone"
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column("store_id", Integer, nullable = False)
    timezone_str = Column("timezone_str", String, nullable = False)

class Report(Base):
    """
    Schema for containing reports

    id : unique id for records.
    report_id : unique id for the report that is being created or finished.
    status : status of the report i.e., (Running, Completed, Failed).
    created_at : time of the creation of report.
    completed_at : time of the completion of report.
    file_path : file path of the csv if the report is created successfully.
    """
    __tablename__ = "reports"

    id = Column(Integer, primary_key = True, autoincrement = True)
    report_id = Column("report_id", String, nullable = False)
    status = Column("status", String, nullable = False)
    created_at = Column("created_at", DateTime, nullable = False, default = datetime.datetime.utcnow())
    completed_at = Column("completed_at", DateTime, nullable = True)
    file_path = Column("file_path", String, nullable = True)


def get_engine_session(db_url : str = "sqlite:///store_monitoring.db"):
    engine = create_engine(db_url)
    Session = sessionmaker(bind = engine)
    return engine, Session
