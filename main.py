from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from allmodels.modelsV4 import *
from sadeq_auto_spare_parts_database import create_database_and_tables
from routers import Product as ProductRouter
from routers import Category as CategoryRouter
from routers import Warehouse as WarehouseRouter
from routers import Customer as CustomerRouter
from routers import Supplier as SupplierRouter
from routers import stock as StockRouter
from routers import Transactions as TransactionsRouter

app = FastAPI(title="Sadeq Auto Spare Parts API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], )

app.include_router(ProductRouter.router, prefix="/apiV4/Products")
app.include_router(CategoryRouter.router, prefix= "/apiV4/Categories")
app.include_router(WarehouseRouter.router, prefix= "/apiV4/Warehouses")
app.include_router(CustomerRouter.router, prefix= "/apiV4/Customers")
app.include_router(SupplierRouter.router,prefix="/apiV4/Suppliers")
app.include_router(StockRouter.router,prefix="/apiV4/Stock")
app.include_router(TransactionsRouter.router,prefix="/apiV4/Transactions")
@app.on_event("startup")
def on_startup():   
    create_database_and_tables()

@app.get("/")
def root():
    return {"message": "System Running"}
