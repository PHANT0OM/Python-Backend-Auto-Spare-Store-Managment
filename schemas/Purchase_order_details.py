from sqlmodel import SQLModel
from typing import Optional
from decimal import Decimal
from pydantic import field_validator

class ProductRead(SQLModel):
    id: int
    name: str
    price: Optional[int] = None
    model_config = {"from_attributes": True}


class PurchaseOrderDetailsBase(SQLModel):
    
    product_id: int
    purchase_order_id : int
    unit_cost: Decimal
    quantity: int
    



class PurchaseOrderDetailsCreate(PurchaseOrderDetailsBase):
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0: 
            raise ValueError("Quantity must be greater than zero.")
        return value



class PurchaseOrderDetailsUpdate(SQLModel): 

    purchase_order_id : int
    product_id: int
    quantity: Optional[int] = None
    unit_cost: Optional[Decimal] = None
    
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return value


class PurchaseOrderDetailsRead(PurchaseOrderDetailsBase):
    product: ProductRead
    model_config = {
        "from_attributes": True 
    }