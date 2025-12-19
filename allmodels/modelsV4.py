from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import date
from sqlalchemy import Column, Integer, ForeignKey

class Category(SQLModel, table=True):
    __tablename__ = "Category"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    name: str = Field(index=True, unique=True, sa_column_kwargs={"name": "Name"}) # Added unique=True

    products: List["Product"] = Relationship(back_populates="category")


class Supplier(SQLModel, table=True):
    __tablename__ = "Supplier"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    name: str = Field(index=True, sa_column_kwargs={"name": "Name"})
    phone: Optional[str] = Field(default=None, sa_column_kwargs={"name": "Phone"})

    products: List["Product"] = Relationship(back_populates="supplier")
  


class Customer(SQLModel, table=True):
    __tablename__ = "Customer"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    name: str = Field(index=True, sa_column_kwargs={"name": "Name"})
    phone: Optional[str] = Field(default=None, sa_column_kwargs={"name": "Phone"})

    orders: List["Order"] = Relationship(back_populates="customer")


class Warehouse(SQLModel, table=True):
    __tablename__ = "Warehouse"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    name: str = Field(sa_column_kwargs={"name": "Name"})

    stock_items: List["Stock"] = Relationship(back_populates="warehouse")


class Product(SQLModel, table=True):
    __tablename__ = "Product"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    name: str = Field(index=True, unique=True, sa_column_kwargs={"name": "Name"}) # Added unique
    origin: str = Field(sa_column_kwargs={"name": "Origin"})
    cost: Decimal = Field(sa_column_kwargs={"name": "Cost"})
    price: Decimal = Field(sa_column_kwargs={"name": "Price"})

    # Mapped category_id to CategoryID
    category_id: Optional[int] = Field(foreign_key="Category.ID", sa_column_kwargs={"name": "CategoryID"})
    # Mapped supplier_id to SupplierID
    supplier_id: Optional[int] = Field(foreign_key="Supplier.ID", sa_column_kwargs={"name": "SupplierID"})

    category: Optional[Category] = Relationship(back_populates="products")
    supplier: Optional[Supplier] = Relationship(back_populates="products")

    order_details: List["OrderDetail"] = Relationship(back_populates="product")
    stock_items: List["Stock"] = Relationship(back_populates="product")
    

class Order(SQLModel, table=True):
    __tablename__ = "Orders"

    id: int = Field(primary_key=True, sa_column_kwargs={"name": "ID","autoincrement": False})
    order_date: date = Field(sa_column_kwargs={"name": "OrderDate"})
    total_amount: Decimal = Field(sa_column_kwargs={"name": "TotalAmount"})
    
    # Mapped customer_id to CustomerID
    customer_id: Optional[int] = Field(foreign_key="Customer.ID", sa_column_kwargs={"name": "CustomerID"})

    customer: Optional[Customer] = Relationship(back_populates="orders")
    details: List["OrderDetail"] = Relationship(back_populates="order")



class Stock(SQLModel, table=True):
    __tablename__ = "Stock"

    # Composite keys mapped to PascalCase columns
    product_id: int = Field(primary_key=True, sa_column_kwargs={"name": "ProductID"},sa_column_args=[ForeignKey("Product.ID")])
    warehouse_id: int = Field(primary_key=True, sa_column_kwargs={"name": "WarehouseID"},sa_column_args=[ForeignKey("Warehouse.ID")])
    quantity: int = Field(sa_column_kwargs={"name": "Quantity"})

    product: Product = Relationship(back_populates="stock_items")
    warehouse: Warehouse = Relationship(back_populates="stock_items")


class OrderDetail(SQLModel, table=True):
    __tablename__ = "OrderDetails"

    order_id: int = Field( primary_key=True, sa_column_kwargs={"name": "OrderID"},sa_column_args=[ForeignKey("Orders.ID")])
    product_id: int = Field( primary_key=True, sa_column_kwargs={"name": "ProductID"},sa_column_args=[ForeignKey("Product.ID")])
    price: Decimal = Field(sa_column_kwargs={"name": "Price"})
    quantity: int = Field(sa_column_kwargs={"name": "Quantity"})

    order: Order = Relationship(back_populates="details")
    product: Product = Relationship(back_populates="order_details")



