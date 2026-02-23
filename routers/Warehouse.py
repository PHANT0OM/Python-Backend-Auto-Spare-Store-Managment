from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Warehouse  
from schemas.Warehouse import WarehouseCreate,WarehouseRead,WarehouseUpdate
from sadeq_auto_spare_parts_database import Get_Session


router  = APIRouter()


@router.get("/ReadWarehouses",response_model=list[WarehouseRead], status_code=200)
def read_warehouses(session: Session = Depends(Get_Session)):


    Warehouses =  session.exec(select(Warehouse)).all()
    return Warehouses 

@router.post("/CreateWarehouse", response_model=WarehouseCreate, status_code=status.HTTP_201_CREATED)
def create_warehouse(warehouse: WarehouseCreate, session: Session = Depends(Get_Session)):
  
    db_Warehouse = Warehouse.model_validate(warehouse)
    
    try:
        session.add(db_Warehouse)
        session.commit()
        session.refresh(db_Warehouse)
        return db_Warehouse
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="A Warehouse with this ID or Name already exists."
        )