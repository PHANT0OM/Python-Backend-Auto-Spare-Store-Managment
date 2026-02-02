from sqlmodel import SQLModel
from typing import Optional
from decimal import Decimal
from pydantic import field_validator

# Forward reference for Product details
#try:
 #   from schemas.Product import ProductRead
#except ImportError:
 #   ProductRead = None

#class TransactionDetailsBase(SQLModel):
  #  product_id: int       # Part of Composite PK
   # price: Decimal        # SQL: decimal(10,2)
    #quantity: int         # SQL: int

#class TransactionDetailsCreate(TransactionDetailsBase):
    # INPUT ONLY: Required for your stock logic, but NOT saved to DB
    #warehouse_id: int 

    #@field_validator("quantity")
    #@classmethod
    #def validate_quantity(cls, value: int) -> int:
    #    if value <= 0:
    #        raise ValueError("Quantity must be greater than zero.")
    #    return value

#class TransactionDetailsRead(TransactionDetailsBase):
#    transaction_id: int   # Part of Composite PK
    
    # Nested Relation: Show Product Name instead of just ID
    #product: Optional["ProductRead"] = None

    #model_config = {"from_attributes": True}