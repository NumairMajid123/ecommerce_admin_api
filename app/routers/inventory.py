from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.models.sales import Product
from app.models.inventory import InventoryLog, LowStockAlert, StockChangeType
from app.schemas.inventory import (
  InventoryStatus,
  InventoryUpdate,
  InventoryLog as InventoryLogSchema,
  LowStockAlert as LowStockAlertSchema,
  LowStockAlertCreate
)
from main import get_db

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/status", response_model=List[InventoryStatus])
def get_inventory_status(
  category: Optional[str] = None,
  low_stock_only: bool = False,
  db: Session = Depends(get_db)
):
  """
  Get current inventory status with optional filters for category and low stock items.
  """
  query = db.query(Product)
  
  if category:
    query = query.filter(Product.category == category)
  
  products = query.all()
  result = []
  
  for product in products:
    low_stock_threshold = (
      product.low_stock_alert.threshold if product.low_stock_alert else None
    )
    needs_restock = (
      product.stock <= low_stock_threshold if low_stock_threshold else False
    )
    
    if low_stock_only and not needs_restock:
      continue
        
    result.append(
      InventoryStatus(
        product_id=product.id,
        name=product.name,
        current_stock=product.stock,
        low_stock_threshold=low_stock_threshold,
        needs_restock=needs_restock,
        last_updated=product.updated_at
      )
    )
  
  return result

@router.post("/update/{product_id}", response_model=InventoryLogSchema)
def update_inventory(
  product_id: int,
  update: InventoryUpdate,
  db: Session = Depends(get_db)
):
  """
  Update inventory levels for a product and log the change.
  """
  product = db.query(Product).filter(Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  previous_quantity = product.stock
  new_quantity = previous_quantity + update.quantity_change
  
  if new_quantity < 0:
    raise HTTPException(
      status_code=400,
      detail="Invalid quantity change: would result in negative stock"
    )
  
  # Create inventory log
  inventory_log = InventoryLog(
    product_id=product_id,
    change_type=update.change_type,
    quantity_change=update.quantity_change,
    previous_quantity=previous_quantity,
    new_quantity=new_quantity,
    notes=update.notes
  )
  
  # Update product stock
  product.stock = new_quantity
  product.updated_at = datetime.utcnow()
  
  db.add(inventory_log)
  db.commit()
  db.refresh(inventory_log)
  
  return inventory_log

@router.get("/history/{product_id}", response_model=List[InventoryLogSchema])
def get_inventory_history(
  product_id: int,
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_db)
):
  """
  Get inventory change history for a specific product.
  """
  product = db.query(Product).filter(Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  logs = db.query(InventoryLog).filter(
    InventoryLog.product_id == product_id
  ).order_by(
    InventoryLog.timestamp.desc()
  ).offset(skip).limit(limit).all()
  
  return logs

@router.post("/alerts", response_model=LowStockAlertSchema)
def set_low_stock_alert(
  alert: LowStockAlertCreate,
  db: Session = Depends(get_db)
):
  """
  Set or update a low stock alert threshold for a product.
  """
  product = db.query(Product).filter(Product.id == alert.product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  existing_alert = db.query(LowStockAlert).filter(
    LowStockAlert.product_id == alert.product_id
  ).first()
  
  if existing_alert:
    existing_alert.threshold = alert.threshold
    existing_alert.is_active = alert.is_active
    db.commit()
    db.refresh(existing_alert)
    return existing_alert
  
  new_alert = LowStockAlert(**alert.dict())
  db.add(new_alert)
  db.commit()
  db.refresh(new_alert)
  
  return new_alert

@router.get("/alerts", response_model=List[LowStockAlertSchema])
def get_low_stock_alerts(
  active_only: bool = True,
  db: Session = Depends(get_db)
):
  """
  Get all low stock alerts, optionally filtering for active ones only.
  """
  query = db.query(LowStockAlert)
  if active_only:
    query = query.filter(LowStockAlert.is_active == True)
  
  return query.all() 