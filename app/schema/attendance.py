from pydantic import BaseModel
from datetime import date


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: str


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceOut(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
