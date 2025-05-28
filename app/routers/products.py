from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.sales import Product
from app.schemas.sales import Product as ProductSchema, ProductCreate
from main import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
def get_products(
  category: Optional[str] = None,
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(get_db)
):
  """
  Get all products with optional category filter and pagination
  """
  query = db.query(Product)
  if category:
    query = query.filter(Product.category == category)
  return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
  """
  Get a specific product by ID
  """
  product = db.query(Product).filter(Product.id == product_id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Product not found")
  return product

@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
  """
  Create a new product
  """
  db_product = Product(**product.dict())
  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
  product_id: int,
  product: ProductCreate,
  db: Session = Depends(get_db)
):
  """
  Update an existing product
  """
  db_product = db.query(Product).filter(Product.id == product_id).first()
  if not db_product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  for key, value in product.dict().items():
    setattr(db_product, key, value)
  
  db_product.updated_at = datetime.utcnow()
  db.commit()
  db.refresh(db_product)
  return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
  """
  Delete a product
  """
  db_product = db.query(Product).filter(Product.id == product_id).first()
  if not db_product:
    raise HTTPException(status_code=404, detail="Product not found")
  
  db.delete(db_product)
  db.commit()
  return {"message": "Product deleted successfully"} 