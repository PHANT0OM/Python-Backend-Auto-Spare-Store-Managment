from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Customer  
from schemas.Customer import CustomerCreate,CustomerRead,CustomerUpdate
from sadeq_auto_spare_parts_database import Get_Session

router = APIRouter()

@router.get("/CustomerRead",response_model=list[CustomerRead],status_code=200)

def read_customers(session: Session = Depends(Get_Session)):

    customers = session.exec(select(Customer)).all()
    return customers 

@router.post("/CreateCustomer", response_model=CustomerCreate, status_code=201)
def create_Customer(product_data: CustomerCreate, session: Session = Depends(Get_Session)):

    
    db_customer = Customer.model_validate(product_data)
    
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    
    return db_customer

@router.put("/UpdateCustomers", response_model=CustomerRead)
def update_Customer(customer_id: int, customer_update: CustomerUpdate, session: Session = Depends(Get_Session)):
 
    db_customers = session.get(Customer, customer_id)   
    if not db_customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_update = customer_update.model_dump(exclude_unset=True)

    for key, value in customer_update.items():

        if key == "id":
            continue
        setattr(db_customers, key, value)

    session.add(db_customers)
    session.commit()
    session.refresh(db_customers)

    return db_customers