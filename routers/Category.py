from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from allmodels.modelsV4 import Category  
from schemas.Category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryReadProducts
from sadeq_auto_spare_parts_database import Get_Session

router = APIRouter()

@router.post("/CreateCategory", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, session: Session = Depends(Get_Session)):
  
    db_category = Category.model_validate(category)
    
    try:
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category
    except:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="A Category with this ID or Name already exists."
        )
    
@router.get("/ReadCategories", response_model=List[CategoryRead])
def read_categories(

    session: Session = Depends(Get_Session)
):

    categories = session.exec(select(Category)).all()
    return categories


@router.get("/CategoriesById", response_model=CategoryReadProducts)
def read_category(category_id: int, session: Session = Depends(Get_Session)):

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category 