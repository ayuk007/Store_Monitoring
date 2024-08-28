from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from src.database.schemas import get_engine_session, Report
from src.report_generator import ReportGenerator
import uuid

app = FastAPI()
report_status = {}

@app.post("/trigger_report/")
async def trigger_report(background_tasks: BackgroundTasks):
    # Generate a unique report_id
    report_id = str(uuid.uuid4())

    engine, Session = get_engine_session()
    session = Session()
    
    report_gen_obj = ReportGenerator()

    # Start the report generation process in the background
    # Generate a unique report_id
    report_id = str(uuid.uuid4())
    # Save the report status in the database
    new_report = Report(report_id=report_id, status="Running")
    session.add(new_report)
    session.commit()
    session.close()
    # Start the report generation process in the background
    background_tasks.add_task(report_gen_obj.generate_report, report_id)
    
    return {"report_id": report_id}

@app.post("/get_report")
async def get_report(report_id: str):
    engine, Session = get_engine_session()
    session = Session()
    
    
    report_id = ''.join(report_id.split("%22"))

    report = session.query(Report).filter(Report.report_id == report_id).first()
    session.close()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if report.status != "Completed":
        raise HTTPException(status_code=400, detail="Report is not yet completed")

    return FileResponse(path=report.file_path, filename=f"{report_id}.csv", media_type='text/csv')