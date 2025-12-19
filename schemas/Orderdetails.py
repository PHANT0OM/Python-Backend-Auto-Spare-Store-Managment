from sqlmodel import SQLModel
from typing import Optional
from decimal import Decimal
from pydantic import field_validator

class ProductRead(SQLModel):
    id: int
    name: str
    price: Optional[int] = None 
    model_config = {"from_attributes": True}

class OrderdetailsBase(SQLModel):

    order_id: int 
    product_id: int
    price: Decimal 
    quantity: int
    


class OrderDetailsCreate(OrderdetailsBase):

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0: 
            raise ValueError("Quantity must be greater than zero.")
        return value


class OrderdetailsUpdate(SQLModel): 

    order_id: int 
    product_id: int
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return value



class OrderDetailsRead(OrderdetailsBase):

    product: ProductRead
    model_config = {"from_attributes": True }