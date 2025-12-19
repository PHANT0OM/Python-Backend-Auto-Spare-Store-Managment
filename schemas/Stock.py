from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator


class ProductRead(SQLModel):
    name : str
class WarehouseRead(SQLModel):
    name : str


class StockBase(SQLModel):
    product_id: int 
    warehouse_id: int
    quantity: int = Field(default=0) 

class StockCreate(StockBase):
    
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value


class StockUpdate(SQLModel):
    quantity: int 

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:

        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value


class StockRead(StockBase):
    product : ProductRead
    warehouse : WarehouseRead
    
    model_config = {
        "from_attributes": True 
    }