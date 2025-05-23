from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from main import Base
import enum

class StockChangeType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
    RETURN = "return"

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change_type = Column(String, nullable=False)
    quantity_change = Column(Integer, nullable=False)  # Positive for additions, negative for reductions
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory_logs")

class LowStockAlert(Base):
    __tablename__ = "low_stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    threshold = Column(Integer, nullable=False)
    is_active = Column(bool, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="low_stock_alert") 