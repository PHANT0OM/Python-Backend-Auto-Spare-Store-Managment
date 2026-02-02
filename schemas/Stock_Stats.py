from sqlmodel import Session, select, func
from allmodels.modelsV4 import Product, Stock 

def get_inventory_stats(session: Session):

    statement_value = (
        select(func.sum(Product.cost * Stock.quantity))
        .join(Stock, Product.id == Stock.product_id)  
    )
    total_value = session.exec(statement_value).first() or 0.0
    statement_count = select(func.count(Product.id))
    total_count = session.exec(statement_count).first() or 0

    return {
        "total_value": total_value,
        "total_count": total_count
    }