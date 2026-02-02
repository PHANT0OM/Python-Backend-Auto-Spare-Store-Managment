from sqlmodel import SQLModel, Field
from decimal import Decimal
from typing import Optional


class CategoryRead(SQLModel):
    name: str 

class SupplierRead(SQLModel):

    name: str 

class ProductBase(SQLModel):
    name: str 
    origin: str
    code : Optional[str] 
    cost: Decimal
    price: Optional[Decimal] 
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(SQLModel):
    name : Optional[str] = None
    origin : Optional[str] = None
    code : Optional[str] = None
    cost : Optional[Decimal] = None
    price : Optional[Decimal] = None
    category_id : Optional[int] = None
    supplier_id : Optional[int] = None

class ProductRead(ProductBase):
    id: int 
    category_name: Optional[CategoryRead] = None
    supplier_name: Optional[SupplierRead] = None
