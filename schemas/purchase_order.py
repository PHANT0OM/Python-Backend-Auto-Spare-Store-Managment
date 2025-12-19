from sqlmodel import SQLModel,Field
from typing import Optional, List
from datetime import date
from decimal import Decimal

class SupplierRead(SQLModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

class PurchaseOrderDetailsRead(SQLModel):

    purchase_order_id : int
    product_id: int
    quantity: int
    unit_cost: Decimal
    model_config = {"from_attributes": True}


class PurchaseOrderBase(SQLModel):

    id: int 
    total_amount: Decimal
    shipping_cost : Decimal 
    order_date : date = Field(default_factory=date.today)
    supplier_id: int


class PurchaseOrderCreate(PurchaseOrderBase):
    pass 



class PurchaseOrderUpdate(SQLModel):  
    id: Optional[int] = None
    total_amount: Optional[Decimal] = None 
    shipping_cost : Optional[Decimal] = None
    order_date: Optional[date] = None
    supplier_id: Optional[int] = None

class PurchaseOrderRead(PurchaseOrderBase):

    
    total_amount: Decimal 
    supplier: SupplierRead
    details: List[PurchaseOrderDetailsRead] = []
    model_config = { "from_attributes": True 
    }