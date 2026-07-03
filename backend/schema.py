from pydantic import BaseModel

class Attendance_Create(BaseModel):
    employee_id : str
    action: str
