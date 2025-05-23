from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total_amount: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sale_date: datetime
    product: Product

    class Config:
        from_attributes = True

class SalesAnalytics(BaseModel):
    total_revenue: float
    total_sales: int
    average_order_value: float
    period_start: datetime
    period_end: datetime

class CategoryAnalytics(BaseModel):
    category: str
    total_revenue: float
    total_sales: int
    average_order_value: float

class TimeSeriesData(BaseModel):
    date: datetime
    revenue: float
    sales_count: int 