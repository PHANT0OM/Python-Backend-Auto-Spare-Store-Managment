from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import date
from sqlalchemy import Column, Integer, ForeignKey,Numeric
import sqlalchemy as sa
class Customer(SQLModel, table=True):
    __tablename__ = "Customer"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    name: str = Field(sa_column=Column("name", sa.NVARCHAR(50), index=True, nullable=False))
    phone: str = Field(sa_column=Column("phone", sa.NVARCHAR(20), nullable=False))
    balance: Decimal = Field(default=Decimal(0), sa_column=Column("balance", Numeric(10, 2), nullable=False, server_default="0.00"))
    transactions: List["Transactions"] = Relationship(back_populates="customer")


class Warehouse(SQLModel, table=True):
    __tablename__ = "Warehouse"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    name: str = Field(sa_column=Column("name", sa.NVARCHAR(150), unique=True, nullable=False))
    stock_items: List["Stock"] = Relationship(back_populates="warehouse")

class Category(SQLModel, table=True):
    __tablename__ = "Category"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    name: str = Field(sa_column=Column("name", sa.NVARCHAR(150), unique=True, index=True, nullable=False))
    product: List["Product"] = Relationship(back_populates="category")

class Supplier(SQLModel, table=True):
    __tablename__ = "Supplier"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    name: str = Field(sa_column=Column("name", sa.NVARCHAR(150), index=True, nullable=False))
    phone: str = Field(sa_column=Column("phone", sa.NVARCHAR(20), nullable=False))
    product: List["Product"] = Relationship(back_populates="supplier")

class Product(SQLModel, table=True):
    __tablename__ = "Product"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    name: str = Field(sa_column=Column("name", sa.NVARCHAR(150), index=True, nullable=False))
    origin: str = Field(sa_column=Column("origin", sa.NVARCHAR(50), nullable=False))
    code: Optional[str] = Field(default=None, sa_column=Column("code", sa.NVARCHAR(50), unique=True, nullable=True))
    cost: Decimal = Field(sa_column=Column("cost", Numeric(10, 2), nullable=False))
    price: Optional[Decimal] = Field(default=None, sa_column=Column("price", Numeric(10, 2), nullable=True))
    category_id: Optional[int] = Field(default=None, foreign_key="Category.id", sa_column_kwargs={"name": "category_id"})
    supplier_id: Optional[int] = Field(default=None,foreign_key="Supplier.id", sa_column_kwargs={"name": "supplier_id"})
    category: Optional[Category] = Relationship(back_populates="product")
    supplier: Optional[Supplier] = Relationship(back_populates="product")
    transaction_details: List["Transactionsdetails"] = Relationship(back_populates="product")
    stock_items: List["Stock"] = Relationship(back_populates="product")
    




class Stock(SQLModel, table=True):
    __tablename__ = "Stock"
    product_id: int = Field(primary_key=True, sa_column_kwargs={"name": "product_id"},sa_column_args=[ForeignKey("Product.id")])
    warehouse_id: int = Field(primary_key=True, sa_column_kwargs={"name": "warehouse_id"},sa_column_args=[ForeignKey("Warehouse.id")])
    quantity: int = Field(sa_column_kwargs={"name": "quantity"})

    product: Product = Relationship(back_populates="stock_items")
    warehouse: Warehouse = Relationship(back_populates="stock_items")

class Transactions(SQLModel, table=True):
    __tablename__ = "Transactions"

    id: Optional[int] = Field(default=None,primary_key=True, sa_column_kwargs={"name": "id"})
    transaction_date: date = Field(sa_column_kwargs={"name": "transaction_date"})
    total_amount: Decimal = Field(sa_column_kwargs={"name": "total_amount"})
    customer_id: Optional[int] = Field(foreign_key="Customer.id", sa_column_kwargs={"name": "customer_id"})

    customer: Optional[Customer] = Relationship(back_populates="transactions")
    details: List["Transactionsdetails"] = Relationship(back_populates="transactions")

class Transactionsdetails(SQLModel, table=True):
    __tablename__ = "Transactionsdetails"

    transaction_id: int = Field(default=None, primary_key=True, sa_column_kwargs={"name": "transaction_id"},sa_column_args=[ForeignKey("Transactions.id")])
    product_id: int = Field( primary_key=True, sa_column_kwargs={"name": "product_id"},sa_column_args=[ForeignKey("Product.id")])
    price: Decimal = Field(sa_column_kwargs={"name": "price"})
    quantity: int = Field(sa_column_kwargs={"name": "quantity"})
    transactions: Transactions = Relationship(back_populates="details")
    product: Product = Relationship(back_populates="transaction_details")
    @property
    def product_name(self) -> str:
        return self.product.name if self.product else "Unknown"

    @property
    def total_item_price(self) -> Decimal:
        return (self.price * self.quantity) if self.price else 0
    @property
    def productid(self) -> int:
        """Maps 'product_id' (Database) to 'productid' (Schema)"""
        return self.product_id



