from sqlmodel import SQLModel
from typing import Optional, List

class StockRead(SQLModel):
    pass

class WarehouseBase(SQLModel):
    id: int 
    name : str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    id: Optional[int] = None
    name : Optional [str] = None

class WarehouseRead(WarehouseBase):

    id: int
    stock_items: List[StockRead] = []
    model_config = {
        "from_attributes": True 
    }