from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Transactions, Transactionsdetails, Product , Stock
from schemas.Transactions import TransactionCreate, TransactionRead
from sadeq_auto_spare_parts_database import Get_Session

router = APIRouter()

@router.get("/ReadTransactions", response_model=List[TransactionRead])
def read_transactions(session: Session = Depends(Get_Session)):

    statement = select(Transactions).options(
        selectinload(Transactions.details).selectinload(Transactionsdetails.product),
        selectinload(Transactions.customer)
    )
    
    transactions = session.exec(statement).all()
    return transactions

@router.post("/CreateTransactions", response_model=TransactionRead, status_code=201)
def create_transaction(transaction_data: TransactionCreate, session: Session = Depends(Get_Session)):
    
    txn_dict = transaction_data.model_dump()
    details_data = txn_dict.pop("details", [])

    
    db_transaction = Transactions(**txn_dict)
    db_transaction.total_amount = 0 
    
    session.add(db_transaction)
    session.flush() 

    calculated_total = 0
    
   
    for item in details_data:
        
       
        statement = select(Stock).where(Stock.product_id == item['productid'])
        stock_record = session.exec(statement).first()

        
        if not stock_record:
            session.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"No stock record found for Product ID {item['product_id']}"
            )

        
        if stock_record.quantity < item['quantity']:
            session.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for Product ID {item['product_id']}. Available: {stock_record.quantity}, Requested: {item['quantity']}"
            )

        
        stock_record.quantity -= item['quantity']
        session.add(stock_record)

        
        final_price = item.get('price') 
        
        if final_price is None:
             session.rollback()
             raise HTTPException(status_code=400, detail="Price is required for every item (Bargaining Mode)")

        # --- C. SAVE DETAIL ---
        db_detail = Transactionsdetails(
            transaction_id=db_transaction.id,
            product_id=item['productid'],
            quantity=item['quantity'],
            price=final_price  # <--- Using the bargained price
        )
        
        calculated_total += (final_price * item['quantity'])
        session.add(db_detail)

    # 4. Finalize
    db_transaction.total_amount = calculated_total
    session.add(db_transaction)

    session.commit()
    session.refresh(db_transaction)
    
    return db_transaction



@router.get("/ReadTransactions/{transaction_id}", response_model=TransactionRead)
def read_single_transaction(transaction_id: int, session: Session = Depends(Get_Session)):
    
    statement = select(Transactions).where(Transactions.id == transaction_id).options(
        selectinload(Transactions.details).selectinload(Transactionsdetails.product),
        selectinload(Transactions.customer)
    )
    
    transaction = session.exec(statement).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    return transaction