from pydantic import BaseModel
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    name: str
    email: str
    phone: str
    join_date: date
    department_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
