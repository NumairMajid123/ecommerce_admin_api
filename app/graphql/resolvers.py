from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import sales, inventory
from app.graphql.types import (
  Product, Sale, InventoryLog, LowStockAlert,
  SalesAnalytics, CategoryAnalytics,
  ProductInput, SaleInput, InventoryUpdateInput, LowStockAlertInput
)

async def get_products(
  category: Optional[str] = None,
  db: Session = next(get_db())
) -> List[Product]:
  query = db.query(sales.Product)
  if category:
      query = query.filter(sales.Product.category == category)
  return query.all()

async def get_product(
  id: int,
  db: Session = next(get_db())
) -> Optional[Product]:
  return db.query(sales.Product).filter(sales.Product.id == id).first()

async def get_sales(
  start_date: Optional[datetime] = None,
  end_date: Optional[datetime] = None,
  db: Session = next(get_db())
) -> List[Sale]:
  query = db.query(sales.Sale)
  if start_date and end_date:
    query = query.filter(sales.Sale.sale_date.between(start_date, end_date))
  return query.all()

async def get_inventory_logs(
  product_id: int,
  db: Session = next(get_db())
) -> List[InventoryLog]:
  return db.query(inventory.InventoryLog).filter(
    inventory.InventoryLog.product_id == product_id
  ).order_by(inventory.InventoryLog.timestamp.desc()).all()

async def get_low_stock_alerts(
  active_only: bool = True,
  db: Session = next(get_db())
) -> List[LowStockAlert]:
  query = db.query(inventory.LowStockAlert)
  if active_only:
    query = query.filter(inventory.LowStockAlert.is_active == True)
  return query.all()

async def get_sales_analytics(
  start_date: datetime,
  end_date: datetime,
  db: Session = next(get_db())
) -> SalesAnalytics:
  query = db.query(
    func.sum(sales.Sale.total_amount).label("total_revenue"),
    func.count(sales.Sale.id).label("total_sales")
  ).filter(sales.Sale.sale_date.between(start_date, end_date)).first()

  total_revenue = query.total_revenue or 0
  total_sales = query.total_sales or 0
  avg_order_value = total_revenue / total_sales if total_sales > 0 else 0

  return SalesAnalytics(
    total_revenue=total_revenue,
    total_sales=total_sales,
    average_order_value=avg_order_value,
    period_start=start_date,
    period_end=end_date
  )

async def create_product(
  input: ProductInput,
  db: Session = next(get_db())
) -> Product:
  product = sales.Product(**input.__dict__)
  db.add(product)
  db.commit()
  db.refresh(product)
  return product

async def create_sale(
  input: SaleInput,
  db: Session = next(get_db())
) -> Sale:
  product = db.query(sales.Product).filter(sales.Product.id == input.product_id).first()
  if not product or product.stock < input.quantity:
    raise ValueError("Invalid product or insufficient stock")

  sale = sales.Sale(
    product_id=input.product_id,
    quantity=input.quantity,
    unit_price=input.unit_price,
    total_amount=input.quantity * input.unit_price
  )
  
  product.stock -= input.quantity
  db.add(sale)
  db.commit()
  db.refresh(sale)
  return sale

async def update_inventory(
  input: InventoryUpdateInput,
  db: Session = next(get_db())
) -> InventoryLog:
  product = db.query(sales.Product).filter(sales.Product.id == input.product_id).first()
  if not product:
    raise ValueError("Product not found")

  previous_quantity = product.stock
  new_quantity = previous_quantity + input.quantity_change
  
  if new_quantity < 0:
    raise ValueError("Invalid quantity change: would result in negative stock")
  
  log = inventory.InventoryLog(
    product_id=input.product_id,
    change_type=input.change_type,
    quantity_change=input.quantity_change,
    previous_quantity=previous_quantity,
    new_quantity=new_quantity,
    notes=input.notes
  )

  product.stock = new_quantity
  db.add(log)
  db.commit()
  db.refresh(log)
  return log

async def set_low_stock_alert(
  input: LowStockAlertInput,
  db: Session = next(get_db())
) -> LowStockAlert:
  product = db.query(sales.Product).filter(sales.Product.id == input.product_id).first()
  if not product:
    raise ValueError("Product not found")

  alert = db.query(inventory.LowStockAlert).filter(
    inventory.LowStockAlert.product_id == input.product_id
  ).first()

  if alert:
    alert.threshold = input.threshold
    alert.is_active = input.is_active
  else:
    alert = inventory.LowStockAlert(**input.__dict__)
    db.add(alert)

  db.commit()
  db.refresh(alert)
  return alert
