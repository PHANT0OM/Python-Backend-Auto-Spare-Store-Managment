from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import date




class Category(SQLModel, table=True):
    __tablename__ = "Category"

    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True)

    products: List["Product"] = Relationship(back_populates="category")


class Supplier(SQLModel, table=True):
    __tablename__ = "Supplier"

    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    phone: Optional[str] = None

    products: List["Product"] = Relationship(back_populates="supplier")
    purchase_orders: List["PurchaseOrder"] = Relationship(back_populates="supplier")


class Customer(SQLModel, table=True):
    __tablename__ = "Customer"

    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    phone: Optional[str] = None

    orders: List["Order"] = Relationship(back_populates="customer")


class Warehouse(SQLModel, table=True):
    __tablename__ = "Warehouse"

    id: int = Field(primary_key=True)
    name: str = Field(unique= True)

    stock_items: List["Stock"] = Relationship(back_populates="warehouse")


class Product(SQLModel, table=True):
    __tablename__ = "Product"

    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique= True)
    origin: str
    price: Decimal
    cost: Decimal

    category_id: Optional[int] = Field(foreign_key="Category.ID")
    supplier_id: Optional[int] = Field(foreign_key="Supplier.ID")

    category: Optional[Category] = Relationship(back_populates="products")
    supplier: Optional[Supplier] = Relationship(back_populates="products")

    order_details: List["OrderDetail"] = Relationship(back_populates="product")
    stock_items: List["Stock"] = Relationship(back_populates="product")
    purchase_order_details: List["PurchaseOrderDetail"] = Relationship(back_populates="product")




class Order(SQLModel, table=True):
    __tablename__ = "Orders"

    id: int = Field(primary_key=True)
    order_date: date
    total_amount: Decimal
    customer_id: Optional[int] = Field(foreign_key="Customer.ID")

    customer: Optional[Customer] = Relationship(back_populates="orders")
    details: List["OrderDetail"] = Relationship(back_populates="order")


class PurchaseOrder(SQLModel, table=True):
    __tablename__ = "Purchase_Order"

    id: int = Field(primary_key=True)
    total_amount: Decimal
    shipping_cost: Decimal
    order_date: date
    supplier_id: int = Field(foreign_key="Supplier.ID")

    supplier: Supplier = Relationship(back_populates="purchase_orders")
    details: List["PurchaseOrderDetail"] = Relationship(back_populates="purchase_order")


class Stock(SQLModel, table=True):
    __tablename__ = "Stock"

    product_id: int = Field(foreign_key="Product.ID", primary_key=True)
    warehouse_id: int = Field(foreign_key="Warehouse.ID", primary_key=True)
    quantity: int

    product: Product = Relationship(back_populates="stock_items")
    warehouse: Warehouse = Relationship(back_populates="stock_items")


class OrderDetail(SQLModel, table=True):
    __tablename__ = "OrderDetails"

    order_id: int = Field(foreign_key="Orders.ID", primary_key=True)
    product_id: int = Field(foreign_key="Product.ID", primary_key=True)
    price: Decimal
    quantity: int

    order: Order = Relationship(back_populates="details")
    product: Product = Relationship(back_populates="order_details")


class PurchaseOrderDetail(SQLModel, table=True):
    __tablename__ = "Purchase_Order_Details"

    product_id: int = Field(foreign_key="Product.ID", primary_key=True)
    purchase_order_id: int = Field(foreign_key="Purchase_Order.ID", primary_key=True)
    unit_cost: Decimal
    quantity: int

    purchase_order: PurchaseOrder = Relationship(back_populates="details")
    product: Product = Relationship(back_populates="purchase_order_details")
