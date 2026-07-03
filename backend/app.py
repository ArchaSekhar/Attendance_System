from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from datetime import datetime, timedelta
import schema, models


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return{"message": "Backend is running"}

@app.post("/attendance")
def create_attendance(
    attendance: schema.Attendance_Create,
    db: Session = Depends(get_db)
):
    new_record = models.Attendance(
        employee_id =attendance.employee_id,
        action=attendance.action
    )

    db.add(new_record)
    db.commit()

    return{
        "message": "Attendance recorded successfully"
    }

@app.get("/attendance/today")
def get_today_attendance(db: Session = Depends(get_db)):
    today = datetime.now().date()

    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = start_of_day + timedelta(days=1)

    records = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.timestamp >= start_of_day,
            models.Attendance.timestamp < end_of_day
        )
        .all()
    )

    return records
