from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class StockChangeType(str, Enum):
  PURCHASE = "purchase"
  SALE = "sale"
  ADJUSTMENT = "adjustment"
  RETURN = "return"

class InventoryLogBase(BaseModel):
  product_id: int
  change_type: StockChangeType
  quantity_change: int
  notes: Optional[str] = None

class InventoryLogCreate(InventoryLogBase):
  pass

class InventoryLog(InventoryLogBase):
  id: int
  previous_quantity: int
  new_quantity: int
  timestamp: datetime

  class Config:
    from_attributes = True

class LowStockAlertBase(BaseModel):
  product_id: int
  threshold: int = Field(gt=0)
  is_active: bool = True

class LowStockAlertCreate(LowStockAlertBase):
  pass

class LowStockAlert(LowStockAlertBase):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
      from_attributes = True

class InventoryStatus(BaseModel):
  product_id: int
  name: str
  current_stock: int
  low_stock_threshold: Optional[int]
  needs_restock: bool
  last_updated: datetime

class InventoryUpdate(BaseModel):
  quantity_change: int
  change_type: StockChangeType
  notes: Optional[str] = None
