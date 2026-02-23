from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload

from allmodels.modelsV4 import Stock, Product, Warehouse
from schemas.Stock import StockCreate, StockRead, StockUpdate, PaginatedStockRead
from sadeq_auto_spare_parts_database import Get_Session
import schemas.Stock_Stats as Stock_Stats
from sqlmodel import or_, func


router = APIRouter()

@router.get("/ReadStock", response_model=PaginatedStockRead)
def read_stock(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(Get_Session)
):
    # Base query for counting totals
    count_statement = select(func.count(Stock.product_id))

    # Base query fetching items with relationships
    statement = select(Stock).options(
        selectinload(Stock.product), 
        selectinload(Stock.warehouse)
    )

    # Get total count before pagination
    total = session.exec(count_statement).one()

    # Apply pagination
    # Assuming order by product_id and then warehouse_id for deterministic results
    statement = statement.order_by(Stock.product_id.desc(), Stock.warehouse_id.desc()).offset(skip).limit(limit)

    stock = session.exec(statement).all()
    
    return PaginatedStockRead(
        items=stock,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/SearchStock/{search}", response_model=PaginatedStockRead)
def search_stock(
    search: str,
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(Get_Session)
):
    # Base query for fetching items with relationships
    statement = select(Stock).join(Product).join(Warehouse).options(
        selectinload(Stock.product), 
        selectinload(Stock.warehouse)
    )

    # Apply search filter (search by product name, product code, or warehouse name)
    search_filter = or_(
        Product.name.contains(search),
        Product.code.contains(search),
        Warehouse.name.contains(search)
    )
    statement = statement.where(search_filter)

    # Base query for counting totals
    count_statement = select(func.count(Stock.product_id)).join(Product).join(Warehouse).where(search_filter)

    # Get total count before pagination
    total = session.exec(count_statement).one()

    # Apply pagination and sorting
    statement = statement.order_by(Stock.product_id.desc(), Stock.warehouse_id.desc()).offset(skip).limit(limit)

    stock = session.exec(statement).all()
    
    return PaginatedStockRead(
        items=stock,
        total=total,
        skip=skip,
        limit=limit
    )


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