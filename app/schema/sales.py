from pydantic import BaseModel
from datetime import date


class SaleBase(BaseModel):
    employee_id: int
    amount: float
    date: date


class SaleCreate(SaleBase):
    pass


class SaleOut(SaleBase):
    id: int

    class Config:
        orm_mode = True
