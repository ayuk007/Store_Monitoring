from app.src.database.schemas import StoreStatus, StoreTimezone, BusinessHours, Base, Report, get_engine_session

engine, Session = get_engine_session()
session = Session()

Base.metadata.create_all(engine)

session.close()