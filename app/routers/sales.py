from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from typing import List, Optional
from dateutil.relativedelta import relativedelta

from app.models.sales import Sale, Product
from app.schemas.sales import (
  Sale as SaleSchema,
  SaleCreate,
  SalesAnalytics,
  CategoryAnalytics,
  TimeSeriesData
)
from main import get_db

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", response_model=SaleSchema)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
  product = db.query(Product).filter(Product.id == sale.product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  if product.stock < sale.quantity:
    raise HTTPException(status_code=400, detail="Insufficient stock")
  
  db_sale = Sale(
    product_id=sale.product_id,
    quantity=sale.quantity,
    unit_price=sale.unit_price,
    total_amount=sale.quantity * sale.unit_price
  )
  
  # Update product stock
  product.stock -= sale.quantity
  
  db.add(db_sale)
  db.commit()
  db.refresh(db_sale)
  return db_sale

@router.get("/analytics", response_model=SalesAnalytics)
def get_sales_analytics(
  start_date: datetime = Query(default=None),
  end_date: datetime = Query(default=None),
  db: Session = Depends(get_db)
):
  if not start_date:
    start_date = datetime.utcnow() - timedelta(days=30)
  if not end_date:
    end_date = datetime.utcnow()

  query = db.query(
    func.sum(Sale.total_amount).label("total_revenue"),
    func.count(Sale.id).label("total_sales")
  ).filter(
    Sale.sale_date.between(start_date, end_date)
  ).first()

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

@router.get("/analytics/category", response_model=List[CategoryAnalytics])
def get_category_analytics(
  start_date: datetime = Query(default=None),
  end_date: datetime = Query(default=None),
  db: Session = Depends(get_db)
):
  if not start_date:
    start_date = datetime.utcnow() - timedelta(days=30)
  if not end_date:
    end_date = datetime.utcnow()

  results = db.query(
    Product.category,
    func.sum(Sale.total_amount).label("total_revenue"),
    func.count(Sale.id).label("total_sales")
  ).join(Sale).filter(
    Sale.sale_date.between(start_date, end_date)
  ).group_by(Product.category).all()

  return [
    CategoryAnalytics(
      category=r.category,
      total_revenue=r.total_revenue,
      total_sales=r.total_sales,
      average_order_value=r.total_revenue / r.total_sales if r.total_sales > 0 else 0
    ) for r in results
  ]

@router.get("/analytics/timeline", response_model=List[TimeSeriesData])
def get_sales_timeline(
  period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"]),
  start_date: datetime = Query(default=None),
  end_date: datetime = Query(default=None),
  db: Session = Depends(get_db)
):
  if not start_date:
    start_date = datetime.utcnow() - relativedelta(months=1)
  if not end_date:
    end_date = datetime.utcnow()

  group_by = {
    "daily": [func.date(Sale.sale_date)],
    "weekly": [extract('year', Sale.sale_date), extract('week', Sale.sale_date)],
    "monthly": [extract('year', Sale.sale_date), extract('month', Sale.sale_date)],
    "annual": [extract('year', Sale.sale_date)]
  }[period]

  results = db.query(
    Sale.sale_date,
    func.sum(Sale.total_amount).label("revenue"),
    func.count(Sale.id).label("sales_count")
  ).filter(
    Sale.sale_date.between(start_date, end_date)
  ).group_by(*group_by).order_by(Sale.sale_date).all()

  return [
    TimeSeriesData(
      date=r.sale_date,
      revenue=r.revenue,
      sales_count=r.sales_count
    ) for r in results
  ]
