from fastapi import FastAPI

app = FastAPI()

@app.post('/trigger_report')
def trigger():
    return "Trigger Successfull"

@app.post("/get_report")
def get_report(report_id: str):
    return f"{report_id} fetched successfully"