from sqlmodel import SQLModel
from typing import Optional,List,TYPE_CHECKING
import phonenumbers
from pydantic import field_validator
from datetime import date

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
   
class OrderRead(SQLModel):
    id : int 
    order_date : date
    total_amount : float
    model_config = {"from_attributes" : True}

class CustomerBase(SQLModel):
    
    id : int 
    name : str
    phone : Optional [str] = None

class CustomerCreate(CustomerBase):
    
    @field_validator("phone")
    @classmethod
    def Validate_phone(cls, value : Optional[str] ) -> Optional[str]:
        return validate_phone_number(value)
    
class CustomerUpdate(SQLModel):
    id : Optional[int] = None
    name : Optional[str] = None
    phone : Optional[str] = None
    @field_validator("phone")
    @classmethod
    def Validate_phone(cls, value : Optional[str] ) -> Optional[str]:
        return validate_phone_number(value)
    
class CustomerRead(CustomerBase):
    orders: List[OrderRead] = []
    
    model_config = { "from_attributes": True }
