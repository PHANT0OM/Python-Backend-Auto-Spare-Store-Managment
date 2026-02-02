from sqlmodel import SQLModel
from typing import Optional,List, TYPE_CHECKING
import phonenumbers
from pydantic import field_validator

class ProductRead(SQLModel):
   
    name: str
    price: Optional[int]=None 
    model_config = {"from_attributes": True}    
def validate_phone_number(value : Optional[str]) -> Optional[str]:
    if value is None:
        return value
    try:
        parsed_number = phonenumbers.parse(value, region="EG", keep_raw_input=True) 
    except phonenumbers.NumberParseException as e:
   
        raise ValueError(f"Could not parse phone number: {e}")
          
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError(f"Phone number '{value}' is not a globally valid number.")
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    return formatted_number.replace(" ", "").replace("-","")
    

class SupplierBase(SQLModel):

    name : str
    phone: Optional[str] = None

class SupplierCreate(SupplierBase):
    @field_validator("phone")
    @classmethod

    def Validate_phone(cls, value : Optional[str] ) -> Optional[str]:
          return validate_phone_number(value)
    
    

class SupplierUpdate(SQLModel):

    id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    @field_validator("phone")
    @classmethod

    def Validate_phone(cls, value : Optional[str] ) -> Optional[str]:
          return validate_phone_number(value)
    
class SupplierReadProducts(SupplierBase):
    

    products: List[ProductRead] = []
    
    model_config = {
        "from_attributes": True 
    }

class SupplierRead(SupplierBase):

    id: Optional[int]
    name: str
    model_config = {
        "from_attributes": True 
    }