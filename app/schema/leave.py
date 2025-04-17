from pydantic import BaseModel
from datetime import date


class LeaveBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str


class LeaveCreate(LeaveBase):
    pass


class LeaveOut(LeaveBase):
    id: int

    class Config:
        orm_mode = True
