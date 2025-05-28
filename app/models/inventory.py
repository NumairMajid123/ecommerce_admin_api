from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, Index, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class StockChangeType(str, enum.Enum):
  PURCHASE = "purchase"
  SALE = "sale"
  ADJUSTMENT = "adjustment"
  RETURN = "return"

class InventoryLog(Base):
  __tablename__ = "inventory_logs"

  id = Column(Integer, primary_key=True, index=True)
  product_id = Column(Integer, ForeignKey("products.id"), index=True)
  change_type = Column(String, nullable=False, index=True)
  quantity_change = Column(Integer, nullable=False)  # Positive for additions, negative for reductions
  previous_quantity = Column(Integer, nullable=False)
  new_quantity = Column(Integer, nullable=False)
  notes = Column(String, nullable=True)
  timestamp = Column(DateTime, default=datetime.utcnow, index=True)

  product = relationship("Product", back_populates="inventory_logs")

  __table_args__ = (
    Index('idx_inventory_product_timestamp', 'product_id', 'timestamp'),
    Index('idx_inventory_type_timestamp', 'change_type', 'timestamp'),
  )

class LowStockAlert(Base):
  __tablename__ = "low_stock_alerts"

  id = Column(Integer, primary_key=True, index=True)
  product_id = Column(Integer, ForeignKey("products.id"), unique=True, index=True)
  threshold = Column(Integer, nullable=False)
  is_active = Column(Boolean, default=True, index=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  product = relationship("Product", back_populates="low_stock_alert")

  __table_args__ = (
      Index('idx_active_alerts', 'is_active', 'product_id'),
  )
