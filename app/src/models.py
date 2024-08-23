from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Enum
Base = declarative_base()

class StoreStatus(Base):
    """
    Schema for status of all the stores based on the polls.
    
    id: unique record id
    store_id : unique_id provided to the store.
    status : status of the store as active or inactive.
    timestamp_utc: #TODO
    """
    __tablename__ = 'store_status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column("store_id", Integer, nullable = False)
    status = Column("status", String, nullable = False)
    timestamp_utc = Column("timestamp_utc", DateTime, nullable = False)

class BusinessHours(Base):
    """
    Schema for business hours of the all stores
    
    id: unique record id
    store_id : unique_id provided to the store.
    day_of_week : refers to the day of the week. 0: Monday  6: Sunday.
    start_time_local : starting time of the store as local time zone.
    end_time_local : closing time of the store as local time zone.
    """
    __tablename__ = 'business_hours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column("store_id", Integer, nullable = False)
    day_of_week = Column("day_of_week", Integer, nullable = False)
    start_time_local = Column("start_time_local", DateTime, nullable = False)
    end_time_local = Column("end_time_local", DateTime, nullable = False)

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

