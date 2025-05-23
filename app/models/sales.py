from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from main import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    sale_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="sales")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sales = relationship("Sale", back_populates="product")
    inventory_logs = relationship("InventoryLog", back_populates="product")
    low_stock_alert = relationship("LowStockAlert", back_populates="product", uselist=False) 