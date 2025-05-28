from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

app = FastAPI(
  title="E-commerce Admin API",
  description="API for e-commerce admin dashboard with sales analytics and GraphQL support",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

from app.models.sales import Base as SalesBase
from app.models.inventory import Base as InventoryBase
SalesBase.metadata.create_all(bind=engine)
InventoryBase.metadata.create_all(bind=engine)

from app.routers.products import router as products_router
from app.routers.sales import router as sales_router
from app.routers.inventory import router as inventory_router

app.include_router(products_router)
app.include_router(sales_router)
app.include_router(inventory_router)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
  return {
    "message": "Welcome to E-commerce Admin API",
    "docs": "/docs",
    "redoc": "/redoc",
    "graphql": "/graphql"
}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
