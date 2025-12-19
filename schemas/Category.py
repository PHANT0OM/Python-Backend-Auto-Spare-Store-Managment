from sqlmodel import SQLModel
from typing import Optional, List


class ProductRead(SQLModel):
   
    id: int
    name: str
    price: Optional[int]=None 
    
    model_config = {"from_attributes": True}



class CategoryBase(SQLModel):

    id : int
    name: str 


class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    id : Optional[int] = None
    name: Optional[str] = None

class CategoryRead(CategoryBase):
     model_config = {
        "from_attributes": True 
    }

class CategoryReadProducts(CategoryBase):
    
    products: List[ProductRead] = []
    
    model_config = {
        "from_attributes": True 
    }