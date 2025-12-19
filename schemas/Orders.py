
from sqlmodel import SQLModel
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import field_validator


class CustomerRead(SQLModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

class OrderDetailsRead(SQLModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    model_config = {"from_attributes": True}


class OrderBase(SQLModel):

    
    id: int 
    order_date: date
    total_amount: Decimal
    customer_id: Optional[int] = None
 



class OrderCreate(OrderBase):
    pass 


class OrderUpdate(SQLModel): 
    
    id: Optional[int] = None
    customer_id: Optional[int] = None
    order_date: Optional[date] = None
    status: Optional[str] = None
    total_amount: Optional[Decimal] = None 



class OrderRead(OrderBase):

    total_amount: Decimal 
    customer: CustomerRead
    details: List[OrderDetailsRead] = []

    model_config = { "from_attributes": True }