from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Sale(Base):
  __tablename__ = "sales"

  id = Column(Integer, primary_key=True, index=True)
  product_id = Column(Integer, ForeignKey("products.id"), index=True)
  quantity = Column(Integer)
  unit_price = Column(Float)
  total_amount = Column(Float, index=True)
  sale_date = Column(DateTime, default=datetime.utcnow, index=True)
  
  product = relationship("Product", back_populates="sales")

  __table_args__ = (
      Index('idx_sales_product_date', 'product_id', 'sale_date'),
      Index('idx_sales_date_amount', 'sale_date', 'total_amount'),
  )

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  category = Column(String, index=True)
  price = Column(Float)
  stock = Column(Integer, index=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  sales = relationship("Sale", back_populates="product")
  inventory_logs = relationship("InventoryLog", back_populates="product")
  low_stock_alert = relationship("LowStockAlert", back_populates="product", uselist=False)

  __table_args__ = (
      Index('idx_product_category_stock', 'category', 'stock'),
      Index('idx_product_name_category', 'name', 'category'),
  )
