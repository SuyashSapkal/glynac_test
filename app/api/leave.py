from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Leave
from app.schema.leave import LeaveCreate, LeaveOut
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/leave",
    tags=["Leave"],
)


# GET all leave records
@router.get("/", response_model=List[LeaveOut])
def get_leaves(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Leave).all()


# GET a single leave record by ID
@router.get("/{leave_id}", response_model=LeaveOut)
def get_leave(
    leave_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave record not found")
    return leave


# CREATE a new leave record
@router.post("/", response_model=LeaveOut, status_code=status.HTTP_201_CREATED)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_leave = Leave(**leave.dict())
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


# DELETE a leave record
@router.delete("/{leave_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave(
    leave_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave record not found")
    db.delete(leave)
    db.commit()


# UPDATE a leave record
@router.put("/{leave_id}", response_model=LeaveOut)
def update_leave(
    leave_id: int,
    updated: LeaveCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave record not found")
    for key, value in updated.dict().items():
        setattr(leave, key, value)
    db.commit()
    db.refresh(leave)
    return leave
