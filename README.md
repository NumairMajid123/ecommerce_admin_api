# E-commerce Admin API

A powerful admin API for e-commerce platforms built with FastAPI and PostgreSQL, supporting both REST and GraphQL endpoints.

## Features

- Product Management
- Sales Tracking
- Inventory Management
- Low Stock Alerts
- Sales Analytics
- GraphQL Support

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- Strawberry GraphQL
- Python 3.8+

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce_admin_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_admin
```

5. Setup the database and populate with demo data:
```bash
chmod +x scripts/setup_db.sh
./scripts/setup_db.sh
```

## Running the API

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- REST API: http://localhost:8000
- GraphQL Playground: http://localhost:8000/graphql
- API Documentation: http://localhost:8000/docs

## API Endpoints

### REST API

- Products:
  - GET /products - List all products
  - GET /products/{id} - Get product details
  - POST /products - Create new product
  - PUT /products/{id} - Update product
  - DELETE /products/{id} - Delete product

- Sales:
  - GET /sales - List all sales
  - GET /sales/analytics - Get sales analytics
  - POST /sales - Create new sale

- Inventory:
  - GET /inventory/logs - Get inventory logs
  - GET /inventory/low-stock - Get low stock alerts
  - POST /inventory/update - Update inventory
  - POST /inventory/alerts - Set low stock alert

### GraphQL

Example Queries:
```graphql
query GetProducts {
  products {
    id
    name
    category
    price
    stock
  }
}

query GetSalesAnalytics {
  salesAnalytics {
    totalSales
    averageOrderValue
    topProducts {
      name
      totalSales
    }
  }
}
```

## Demo Data

The setup script populates the database with demo data including:
- Various product categories (Electronics, Home & Kitchen, etc.)
- Sample products with realistic prices and stock levels
- 90 days of historical sales data
- Inventory logs and low stock alerts

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
