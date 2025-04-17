from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Department
from app.schema.department import DepartmentCreate, DepartmentOut
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


# GET all departments
@router.get("/", response_model=List[DepartmentOut])
def get_departments(
    db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    return db.query(Department).all()


# GET single department
@router.get("/{department_id}", response_model=DepartmentOut)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# CREATE a new department
@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_department = Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


# DELETE a department
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(department)
    db.commit()
    return


# UPDATE a department
@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in department_data.dict().items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department
