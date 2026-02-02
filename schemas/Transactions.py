from sqlmodel import SQLModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

class TransactiondetailsBase(SQLModel):
    productid : int
    quantity : int
    price : Optional[Decimal] = None

class TransactiondetailsCreate(TransactiondetailsBase):
    pass

class TransactiondetailsRead(TransactiondetailsBase):
    product_name : Optional[str] = "unknown product"
    total_item_price : Decimal

class TransactionBase(SQLModel):
    transaction_date: date
    total_amount: Decimal = Decimal("0.00") 
    customer_id: Optional[int] = None       
class TransactionCreate(TransactionBase):
    details : list[TransactiondetailsCreate]

class TransactionUpdate(SQLModel):
    transaction_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    customer_id: Optional[int] = None

class TransactionRead(TransactionBase):
    id: int 
    total_amount : Decimal

    details: List[TransactiondetailsRead] = []

    model_config = {"from_attributes": True}