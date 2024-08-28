# Store Monitoring: Loop AI assessment
### Name: Ayush Nashine
### Tools used:
- FastAPI
- SQLAlchemy (ORM)

## Documentation
### Assumptions Taken
- If the business hours doesn't exist in the database, then it'll be open for 24*7 i.e., (00:00:00 AM - 23:59:59 PM), as mentioned in the assessment.

- If the business hours doesn't exist for certain day then it is preassumed to be closed for that day and won't be included in the calculation.

- If the last entry for the day is inactive then from that eentry to the end business hour it's assumed to be inactive and will be included in downtime and vice-versa.

- If the start entry for the day is within business hour and is active then from start business hour to that time it preassumed to be active and included in uptime and vice-versa.

### Last day calculation
- Taken the last day from the maximum time taken.
- Edge Case : Ensured that the total hours should not be greater than 24 hrs.
- Edge Case : Only taken that day into account thich is calculated as one day ago.

### Last Week calculation
- Taken the time from last week to present day into according accorng to the data.

- Edge Case: Ensured that there should be no time overlap between hrs.


## Many of the edge cases handled based on the assumptions made.