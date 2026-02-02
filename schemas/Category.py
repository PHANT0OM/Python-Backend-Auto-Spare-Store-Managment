from sqlmodel import SQLModel
from typing import Optional, List


class ProductRead(SQLModel):
   
    name: str
    price: Optional[int]=None 
    
    model_config = {"from_attributes": True}


class CategoryBase(SQLModel):

    name: str 

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryRead(CategoryBase):
    id : Optional[int]
    products: List[ProductRead] = []
    model_config = {
        "from_attributes": True 
    }

class CategoryReadProducts(CategoryBase):
    
    products: List[ProductRead] = []
    
    model_config = {
        "from_attributes": True 
    }