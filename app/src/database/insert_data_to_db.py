import pandas as pd
from tqdm import tqdm
from app.src.database.schemas import StoreStatus, StoreTimezone, BusinessHours, Base, Report, get_engine_session

status_data = pd.read_csv(r"path_to_store_status_csv")
hours_data = pd.read_csv(r"path_to_menu_hours_csv")
timezone_data = pd.read_csv(r"path_to_store_timezone_csv")
print("Read csv successfully..")

engine, Session = get_engine_session()
session = Session()

# Function to load data into SQL database
def load_data_to_db():

        # Load store status
    for _, row in tqdm(status_data.iterrows(), total=status_data.shape[0], desc="Loading Store Status"):
        status_record = StoreStatus(
            store_id=row['store_id'],
            timestamp_utc=row['timestamp_utc'],
            status=row['status']
        )
        session.add(status_record)

    # Load business hours
    for _, row in tqdm(hours_data.iterrows(), total=hours_data.shape[0], desc="Loading Business Hours"):
        hours_record = BusinessHours(
            store_id=row['store_id'],
            day_of_week=row['day'],
            start_time_local=row['start_time_local'],
            end_time_local=row['end_time_local']
        )
        session.add(hours_record)

    # Load store timezones
    for _, row in tqdm(timezone_data.iterrows(), total=timezone_data.shape[0], desc="Loading Store Timezones"):
        timezone_record = StoreTimezone(
            store_id=row['store_id'],
            timezone_str=row['timezone_str']
        )
        session.add(timezone_record)

    # Commit the transaction to save data to the database
    session.commit()
    session.close()
    
# Call the function to load data
load_data_to_db()