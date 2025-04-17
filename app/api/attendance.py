from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Attendance
from app.schema.attendance import AttendanceCreate, AttendanceOut
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# GET all attendance records
@router.get("/", response_model=List[AttendanceOut])
def get_attendance_records(
    db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    return db.query(Attendance).all()


# GET a specific attendance record
@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return record


# CREATE new attendance record
@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_record = Attendance(**attendance.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


# DELETE an attendance record
@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    db.delete(record)
    db.commit()


# UPDATE an attendance record
@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(
    attendance_id: int,
    updated: AttendanceCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    for key, value in updated.dict().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record
