from typing import List, Optional
import strawberry
from datetime import datetime
from enum import Enum

@strawberry.enum
class StockChangeType(str, Enum):
  PURCHASE = "purchase"
  SALE = "sale"
  ADJUSTMENT = "adjustment"
  RETURN = "return"

@strawberry.type
class Product:
  id: int
  name: str
  category: str
  price: float
  stock: int
  created_at: datetime
  updated_at: datetime

@strawberry.type
class Sale:
  id: int
  product_id: int
  quantity: int
  unit_price: float
  total_amount: float
  sale_date: datetime
  product: Product

@strawberry.type
class InventoryLog:
  id: int
  product_id: int
  change_type: StockChangeType
  quantity_change: int
  previous_quantity: int
  new_quantity: int
  notes: Optional[str]
  timestamp: datetime
  product: Product

@strawberry.type
class LowStockAlert:
  id: int
  product_id: int
  threshold: int
  is_active: bool
  created_at: datetime
  updated_at: datetime
  product: Product

@strawberry.type
class SalesAnalytics:
  total_revenue: float
  total_sales: int
  average_order_value: float
  period_start: datetime
  period_end: datetime

@strawberry.type
class CategoryAnalytics:
  category: str
  total_revenue: float
  total_sales: int
  average_order_value: float

@strawberry.input
class ProductInput:
  name: str
  category: str
  price: float
  stock: int

@strawberry.input
class SaleInput:
  product_id: int
  quantity: int
  unit_price: float

@strawberry.input
class InventoryUpdateInput:
  product_id: int
  change_type: StockChangeType
  quantity_change: int
  notes: Optional[str] = None

@strawberry.input
class LowStockAlertInput:
  product_id: int
  threshold: int
  is_active: bool = True
