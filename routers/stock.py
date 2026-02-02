from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload

from allmodels.modelsV4 import Stock, Product
from schemas.Stock import StockCreate, StockRead, StockUpdate
from sadeq_auto_spare_parts_database import Get_Session
import schemas.Stock_Stats as Stock_Stats


router = APIRouter()

@router.get("/ReadStock", response_model=List[StockRead])
def read_stock(session: Session = Depends(Get_Session)):

    statement = select(Stock).options(
        selectinload(Stock.product), 
        selectinload(Stock.warehouse)
    )
    stock = session.exec(statement).all()
    return stock 


@router.post("/CreateStock", response_model=StockRead, status_code=201)
def create_stock(stock_data: StockCreate, session: Session = Depends(Get_Session)):
    

    existing_stock = session.exec(
        select(Stock).where(
            Stock.product_id == stock_data.product_id,
            Stock.warehouse_id == stock_data.warehouse_id
        )
    ).first()

    if existing_stock:
        raise HTTPException(
            status_code=400, 
            detail="Stock already initialized for this Product in this Warehouse. Use Update instead."
        )


    db_stock = Stock.model_validate(stock_data)
    
    session.add(db_stock)
    session.commit()
    session.refresh(db_stock)
    
    return db_stock


@router.put("/UpdateStock", response_model=StockRead)
def update_stock(
    stock_update: StockUpdate, 
    session: Session = Depends(Get_Session)
):
    
    statement = select(Stock).where(
        Stock.product_id == stock_update.product_id,
        Stock.warehouse_id == stock_update.warehouse_id
    )
    db_stock = session.exec(statement).first()

    if not db_stock:
        raise HTTPException(
            status_code=404, 
            detail="Stock record not found. Please Create it first."
        )

    update_data = stock_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_stock, key, value)

    session.add(db_stock)
    session.commit()
    session.refresh(db_stock)
    
    return db_stock

@router.get("/StockStats")
def read_dashboard_stats(session: Session = Depends(Get_Session)):
    return Stock_Stats.get_inventory_stats(session)