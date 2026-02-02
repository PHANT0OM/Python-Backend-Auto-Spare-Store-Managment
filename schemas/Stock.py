from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator,computed_field


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
    product_id : int
    warehouse_id : int
    quantity: int 
    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:  
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value

class StockRead(StockBase):
    
    product: ProductRead = Field(exclude=True)
    warehouse: WarehouseRead = Field(exclude=True)
    @computed_field
    def product_name(self) -> str:
        return self.product.name

    @computed_field
    def warehouse_name(self) -> str:
        return self.warehouse.name
    model_config = {
        "from_attributes": True 
    }