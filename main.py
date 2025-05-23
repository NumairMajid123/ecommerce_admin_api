from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

# Initialize FastAPI app
app = FastAPI(
    title="E-commerce Admin API",
    description="API for e-commerce admin dashboard with sales analytics and GraphQL support",
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

# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint
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