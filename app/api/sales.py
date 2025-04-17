from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Sales
from app.schema.sales import SaleCreate, SaleOut
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


# GET all sales records
@router.get("/", response_model=List[SaleOut])
def get_sales(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return db.query(Sales).all()


# GET a single sales record
@router.get("/{sales_id}", response_model=SaleOut)
def get_sales_record(
    sales_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    sale = db.query(Sales).filter(Sales.id == sales_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sales record not found")
    return sale


# CREATE a new sales record
@router.post("/", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sales_record(
    sales: SaleCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_sale = Sales(**sales.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale


# DELETE a sales record
@router.delete("/{sales_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sales_record(
    sales_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    sale = db.query(Sales).filter(Sales.id == sales_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sales record not found")
    db.delete(sale)
    db.commit()
    return


# UPDATE a sales record
@router.put("/{sales_id}", response_model=SaleOut)
def update_sales_record(
    sales_id: int,
    sales_data: SaleCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    sale = db.query(Sales).filter(Sales.id == sales_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sales record not found")

    for key, value in sales_data.dict().items():
        setattr(sale, key, value)

    db.commit()
    db.refresh(sale)
    return sale
