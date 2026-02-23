
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List,Optional
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Product  
from schemas.Product import ProductCreate, ProductRead, ProductUpdate, PaginatedProductRead
from sadeq_auto_spare_parts_database import Get_Session
from sqlmodel import or_, func

router = APIRouter()
    
@router.get("/ReadProducts", response_model=PaginatedProductRead)
def read_products(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(Get_Session)
):
    # Base query for counting totals
    count_statement = select(func.count(Product.id))
    
    # Base query for fetching items with relationships
    statement = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.supplier)
    )

    # Get total count before pagination
    total = session.exec(count_statement).one()

    # Apply pagination and sorting
    statement = statement.order_by(Product.id.desc()).offset(skip).limit(limit)

    products = session.exec(statement).all()
    
    return PaginatedProductRead(
        items=products,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/SearchProducts/{search}", response_model=PaginatedProductRead)
def search_products(
    search: str,
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(Get_Session)
):
    # Base query for fetching items with relationships
    statement = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.supplier)
    )

    # Apply search filter
    search_filter = or_(
        Product.name.contains(search),
        Product.code.contains(search)
    )
    statement = statement.where(search_filter)
    
    # Base query for counting totals
    count_statement = select(func.count(Product.id)).where(search_filter)

    # Get total count before pagination
    total = session.exec(count_statement).one()

    # Apply pagination and sorting
    statement = statement.order_by(Product.id.desc()).offset(skip).limit(limit)

    products = session.exec(statement).all()
    
    return PaginatedProductRead(
        items=products,
        total=total,
        skip=skip,
        limit=limit
    )


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