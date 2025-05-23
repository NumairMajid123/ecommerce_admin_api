from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecommerce_admin")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Admin API",
    description="API for e-commerce admin dashboard with sales analytics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models and create tables
from app.models.sales import Base as SalesBase
from app.models.inventory import Base as InventoryBase
SalesBase.metadata.create_all(bind=engine)
InventoryBase.metadata.create_all(bind=engine)

# Import and include routers
from app.routers.sales import router as sales_router
from app.routers.inventory import router as inventory_router
app.include_router(sales_router)
app.include_router(inventory_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Admin API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 