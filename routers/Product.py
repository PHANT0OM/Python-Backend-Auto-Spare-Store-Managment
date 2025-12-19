
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Product  
from schemas.Product import ProductCreate, ProductRead, ProductUpdate
from sadeq_auto_spare_parts_database import Get_Session

router = APIRouter()
    
@router.get("/ReadProducts", response_model=List[ProductRead])
def read_products(session: Session = Depends(Get_Session)):
    statement =  select(Product).options(
        selectinload(Product.category),
        selectinload(Product.supplier)
    )

    products = session.exec(select(Product)).all()
    return products 


@router.post("/CreateProducts", response_model=ProductRead, status_code=201)
def create_product(product_data: ProductCreate, session: Session = Depends(Get_Session)):

    
    db_product = Product.model_validate(product_data)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    
    return db_product

@router.put("/UpdateProducts", response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, session: Session = Depends(Get_Session)):
 
    db_product = session.get(Product, product_id)   
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product_update.model_dump(exclude_unset=True)

    for key, value in product_data.items():

        if key == "id":
            continue
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product