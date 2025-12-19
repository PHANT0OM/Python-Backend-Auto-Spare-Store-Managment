from sqlmodel import SQLModel, Field
from decimal import Decimal
from typing import Optional

class CategoryRead(SQLModel):
    name: str 

class SupplierRead(SQLModel):

    name: str 

class ProductBase(SQLModel):
    id : int
    name: str 
    origin: str 
    cost: Decimal
    price: Decimal 
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    

class ProductCreate(ProductBase):

    pass

class ProductUpdate(SQLModel):
    id : Optional[int] = None
    name : Optional[str] = None
    origin : Optional[str] = None
    cost : Optional[Decimal] = None
    price : Optional[Decimal] = None
    category_id : Optional[int] = None
    supplier_id : Optional[int] = None

class ProductRead(ProductBase):
    id: int 
    category_name: Optional[CategoryRead] = None
    supplier_name: Optional[SupplierRead] = None