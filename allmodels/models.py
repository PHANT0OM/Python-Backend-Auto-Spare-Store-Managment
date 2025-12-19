from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from decimal import Decimal
from datetime import date


class Category(SQLModel, table=True):

    id: int = Field(primary_key=True, alias="ID", schema_extra={"examples": [1]})
    name: str = Field(index=True, alias="Name")
    

    products: List["Product"] = Relationship(back_populates="category")

class Supplier(SQLModel, table=True):

    id: int = Field(primary_key=True, alias="ID") 
    name: str = Field(index=True, alias="Name")
    phone: Optional[str] = Field(default=None, alias="Phone")
    
    products: List["Product"] = Relationship(back_populates="supplier")
    purchase_orders: List["Purchase_order"] = Relationship(back_populates="supplier")

class Customer(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="ID")
    name: str = Field(index=True, alias="Name")
    phone: str = Field(alias="Phone")
    
    orders: List["Orders"] = Relationship(back_populates="customer")

class Warehouse(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="ID")
    name: str = Field(alias="Name")
    
    stock_items: List["Stock"] = Relationship(back_populates="warehouse")



class Product(SQLModel, table=True):

    id: int = Field(primary_key=True, alias="ID") 
    
    name: str = Field(index=True, alias="Name")
    origin: str = Field(alias="Origin")
    price: Decimal = Field(alias="Price") 
    cost: Decimal = Field(alias="Cost")
    
  
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", alias="CategoryID")
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id", alias="SupplierID")
    

    category: Optional["Category"] = Relationship(back_populates="products")
    supplier: Optional["Supplier"] = Relationship(back_populates="products")
    ordersdetails: List["Ordersdetails"] = Relationship(back_populates="product")
    stock_items: List["Stock"] = Relationship(back_populates="product")
    purchase_order_details: List["Purchase_order_details"] = Relationship(back_populates="product")


class Orders(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="ID")
    orderdate: date = Field(alias="OrderDate") 
    totalamount: Decimal = Field(alias="TotalAmount")
    customer_id: int = Field(foreign_key="customer.id", alias="CustomerID")
    
    customer: "Customer" = Relationship(back_populates="orders")
    details: List["Ordersdetails"] = Relationship(back_populates="orders")

class Purchase_order(SQLModel, table=True, tablename="Purchase_Order") :
    id: int = Field(primary_key=True, alias="ID")
    totalamount: Decimal = Field(alias="TotalAmount")
    shippingcost: Decimal = Field(alias="ShippingCost")
    orderdate: date = Field(alias="OrderDate")   
    supplier_ID: int = Field(foreign_key="supplier.id", alias="SupplierID")
    
    supplier: "Supplier" = Relationship(back_populates="purchase_orders")
    details: List["Purchase_order_details"] = Relationship(back_populates="purchase_order")

class Stock(SQLModel, table=True):
    product_id: int = Field(foreign_key="product.id", primary_key=True, alias="ProductID")
    warehouse_id: int = Field(foreign_key="warehouse.id", primary_key=True, alias="WarehouseID")
    quantity: int = Field(alias="Quantity")
    
    product: "Product" = Relationship(back_populates="stock_items")
    warehouse: "Warehouse" = Relationship(back_populates="stock_items")

class Ordersdetails(SQLModel, table=True, tablename="OrderDetails"): 
    order_ID: int = Field(foreign_key="orders.id", primary_key=True, alias="OrderID")
    product_id: int = Field(foreign_key="product.id", primary_key=True, alias="ProductID")
    price: Decimal = Field(alias="Price")
    quantity: int = Field(alias="Quantity")
    
    orders: "Orders" = Relationship(back_populates="details")
    product: "Product" = Relationship(back_populates="ordersdetails")

class Purchase_order_details(SQLModel, table=True, tablename="Purchase_Order_Details"):
    product_id: int = Field(foreign_key="product.id", primary_key=True, alias="ProductID")
    purchase_order_id: int = Field(foreign_key="Purchase_Order.id   ", primary_key=True, alias="PurchaseOrderID")
    unitcost: Decimal = Field(alias="UnitCost")
    quantity: int = Field(alias="Quantity")
    
    purchase_order: "Purchase_order" = Relationship(back_populates="details")
    product: "Product" = Relationship(back_populates="purchase_order_details")