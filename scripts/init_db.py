from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.sales import Product, Sale
from app.models.inventory import InventoryLog, LowStockAlert, StockChangeType

CATEGORIES = [
  "Electronics",
  "Home & Kitchen",
  "Fashion",
  "Books",
  "Sports & Outdoors",
  "Beauty & Personal Care",
  "Toys & Games",
  "Grocery",
]

SAMPLE_PRODUCTS = [
  {"name": "4K Smart TV 55-inch", "category": "Electronics", "price": 499.99, "stock": 50},
  {"name": "Wireless Noise-Canceling Headphones", "category": "Electronics", "price": 199.99, "stock": 100},
  {"name": "Smart Home Security Camera", "category": "Electronics", "price": 79.99, "stock": 150},

  {"name": "Robot Vacuum Cleaner", "category": "Home & Kitchen", "price": 299.99, "stock": 75},
  {"name": "Air Fryer XL", "category": "Home & Kitchen", "price": 129.99, "stock": 120},
  {"name": "Coffee Maker with Grinder", "category": "Home & Kitchen", "price": 159.99, "stock": 85},

  {"name": "Men's Running Shoes", "category": "Fashion", "price": 89.99, "stock": 200},
  {"name": "Women's Yoga Pants", "category": "Fashion", "price": 49.99, "stock": 300},
  {"name": "Leather Wallet", "category": "Fashion", "price": 39.99, "stock": 250},

  {"name": "Bestseller Fiction Book", "category": "Books", "price": 24.99, "stock": 400},
  {"name": "Cooking Recipe Collection", "category": "Books", "price": 34.99, "stock": 150},
  {"name": "Self-Help Guide", "category": "Books", "price": 19.99, "stock": 200},
]

def create_demo_data():
  db = SessionLocal()
  try:
    products = []
    for product_data in SAMPLE_PRODUCTS:
      product = Product(**product_data)
      db.add(product)
      products.append(product)
    db.commit()

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)
    current_date = start_date

    while current_date <= end_date:
      daily_sales = random.randint(5, 15)
      for _ in range(daily_sales):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        
        sale = Sale(
          product_id=product.id,
          quantity=quantity,
          unit_price=product.price,
          total_amount=product.price * quantity,
          sale_date=current_date.replace(
            hour=random.randint(8, 20),
            minute=random.randint(0, 59)
          )
        )
        db.add(sale)

        product.stock -= quantity

        log = InventoryLog(
          product_id=product.id,
          change_type=StockChangeType.SALE,
          quantity_change=-quantity,
          previous_quantity=product.stock + quantity,
          new_quantity=product.stock,
          notes=f"Sale: Order #{sale.id}"
        )
        db.add(log)

      current_date += timedelta(days=1)
    
    for product in products:
      if product.stock < 100:
        alert = LowStockAlert(
          product_id=product.id,
          threshold=50,
          is_active=True
        )
        db.add(alert)

    for product in products:
      if product.stock < 100:
        restock_amount = random.randint(50, 200)
        product.stock += restock_amount
        
        log = InventoryLog(
          product_id=product.id,
          change_type=StockChangeType.PURCHASE,
          quantity_change=restock_amount,
          previous_quantity=product.stock - restock_amount,
          new_quantity=product.stock,
          notes="Regular restock"
        )
        db.add(log)

    db.commit()

  except Exception as e:
    print(f"Error creating demo data: {e}")
    db.rollback()
    raise
  finally:
    db.close()

if __name__ == "__main__":
  Base.metadata.create_all(bind=engine)
  
  create_demo_data()
  print("Demo data created successfully!")
