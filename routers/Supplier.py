from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Supplier  
from schemas.Supplier import SupplierCreate,SupplierRead,SupplierUpdate,SupplierReadProducts
from sadeq_auto_spare_parts_database import Get_Session



router  = APIRouter()

@router.get("/ReadSuppliers", response_model=List[SupplierRead],status_code=201)
def read_suppliers(session: Session = Depends(Get_Session)):
    suppliers = session.exec(select(Supplier)).all()
    return suppliers 


@router.get("/ReadSuppliersWithProducts", response_model=List[SupplierReadProducts],status_code=201)
def read_suppliers(session: Session = Depends(Get_Session)):
    suppliers = session.exec(select(Supplier)).all()
    return suppliers 

@router.post("/CreateSupplier", response_model=SupplierRead,status_code=201)
def create_product(supplier_data: SupplierCreate, session: Session = Depends(Get_Session)):

    
    db_suppliers = Supplier.model_validate(supplier_data)
    
    session.add(db_suppliers)
    session.commit()
    session.refresh(db_suppliers)
    
    return db_suppliers