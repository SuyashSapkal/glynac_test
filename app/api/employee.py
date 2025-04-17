from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Employee
from app.schema.employee import EmployeeCreate, EmployeeOut
from app.api.auth import get_current_user  # Ensures JWT auth

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


# GET all employees
@router.get("/", response_model=List[EmployeeOut])
def get_employees(
    db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    return db.query(Employee).all()


# GET single employee by ID
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# CREATE a new employee
@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# DELETE employee
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return


# UPDATE employee
@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    updated_data: EmployeeCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in updated_data.dict().items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee
