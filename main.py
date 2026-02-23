from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from allmodels.modelsV4 import *
from routers import Product as ProductRouter
from routers import Category as CategoryRouter
from routers import Warehouse as WarehouseRouter
from routers import Customer as CustomerRouter
from routers import Supplier as SupplierRouter
from routers import stock as StockRouter
from routers import Transactions as TransactionsRouter


app = FastAPI(title="Sadeq Auto Spare Parts API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Global Error: {exc}") 
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please contact support if the issue persists."},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
app.include_router(ProductRouter.router, prefix="/apiV4/Products")
app.include_router(CategoryRouter.router, prefix= "/apiV4/Categories")
app.include_router(WarehouseRouter.router, prefix= "/apiV4/Warehouses")
app.include_router(CustomerRouter.router, prefix= "/apiV4/Customers")
app.include_router(SupplierRouter.router,prefix="/apiV4/Suppliers")
app.include_router(StockRouter.router,prefix="/apiV4/Stock")
app.include_router(TransactionsRouter.router,prefix="/apiV4/Transactions")
# Database migrations are now handled via Alembic offline

@app.get("/")
def root():
    return {"message": "System Running"}
