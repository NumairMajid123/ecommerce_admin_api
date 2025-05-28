# E-commerce Admin API

A powerful admin API for e-commerce platforms that provides comprehensive sales analytics, inventory management, and product administration capabilities. This API supports both RESTful and GraphQL interfaces, offering flexibility in how clients interact with the system.

## Technology Stack

### Backend Framework
- **Language**: Python 3.8+
- **Framework**: FastAPI - A modern, fast web framework for building APIs with Python
- **API Types**: 
  - RESTful API with OpenAPI/Swagger documentation
  - GraphQL API using Strawberry GraphQL

### Database
- **Type**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- Features:
  - Optimized indexing for better query performance
  - Proper database normalization
  - Transaction support
  - Foreign key constraints for data integrity

### Dependencies
- FastAPI (0.109.2) - Web framework
- SQLAlchemy (2.0.27) - Database ORM
- Alembic (1.13.1) - Database migrations
- Strawberry GraphQL (0.219.2) - GraphQL support
- Pydantic (2.6.1) - Data validation
- psycopg2-binary (2.9.9) - PostgreSQL adapter
- Additional utilities listed in requirements.txt

## Setup Instructions

1. **Prerequisites**:
   - Python 3.8 or higher
   - PostgreSQL 12 or higher
   - pip (Python package manager)

2. **Clone and Setup**:
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd ecommerce_admin_api

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Configuration**:
   ```bash
   # Create a .env file in the root directory
   cat << EOF > .env
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ecommerce_admin
   EOF
   ```

4. **Database Setup and Demo Data**:
   ```bash
   # Make the setup script executable
   chmod +x scripts/setup_db.sh
   
   # Run the setup script
   ./scripts/setup_db.sh
   ```

5. **Start the Server**:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

### REST API Endpoints

#### Products
- `GET /products`
  - List all products
  - Supports filtering by category and pagination
- `GET /products/{id}`
  - Get detailed product information
- `POST /products`
  - Create a new product
  - Required fields: name, category, price, stock
- `PUT /products/{id}`
  - Update product information
- `DELETE /products/{id}`
  - Remove a product

#### Sales
- `GET /sales`
  - List all sales
  - Supports date range filtering
- `GET /sales/analytics`
  - Get sales analytics
  - Parameters: start_date, end_date
  - Returns: total sales, average order value, top products
- `POST /sales`
  - Create a new sale record
  - Automatically updates inventory

#### Inventory
- `GET /inventory/logs`
  - Get inventory change history
  - Supports filtering by product and date range
- `GET /inventory/low-stock`
  - Get products with low stock alerts
- `POST /inventory/update`
  - Update product inventory
  - Supports different change types (purchase, sale, adjustment)
- `POST /inventory/alerts`
  - Configure low stock alerts for products

### GraphQL API

Available at `/graphql` with an interactive GraphQL Playground.

#### Example Queries
```graphql
# Get products with their current stock
query GetProducts {
  products {
    id
    name
    category
    price
    stock
  }
}

# Get sales analytics
query GetSalesAnalytics {
  salesAnalytics {
    totalSales
    averageOrderValue
    topProducts {
      name
      totalSales
    }
    categoryBreakdown {
      category
      totalSales
      percentageOfTotal
    }
  }
}
```

#### Example Mutations
```graphql
# Create a new product
mutation CreateProduct {
  createProduct(input: {
    name: "New Product"
    category: "Electronics"
    price: 299.99
    stock: 100
  }) {
    id
    name
    stock
  }
}

# Record a sale
mutation CreateSale {
  createSale(input: {
    productId: 1
    quantity: 2
    unitPrice: 299.99
  }) {
    id
    totalAmount
    product {
      name
      stock
    }
  }
}
```

## Demo Data

The system comes pre-populated with demo data including:
- 12 sample products across 4 categories
- 90 days of historical sales data
- Inventory logs for all transactions
- Low stock alerts configuration

## Development

- API Documentation: http://localhost:8000/docs
- GraphQL Playground: http://localhost:8000/graphql
- Alternative API Docs: http://localhost:8000/redoc

## Error Handling

The API implements standard HTTP status codes:
- 200: Successful operation
- 201: Resource created
- 400: Bad request
- 404: Resource not found
- 500: Server error

GraphQL errors are returned in the standard GraphQL error format with detailed messages.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Database Documentation

### Database Schema

The system uses PostgreSQL with a normalized relational database design. Here's a detailed breakdown of each table and their relationships:

#### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_product_category_stock (category, stock),
    INDEX idx_product_name_category (name, category)
);
```
**Purpose**: Central product catalog storage
- Stores basic product information including name, category, and current stock level
- Tracks creation and last update timestamps
- Optimized for category-based queries and stock level monitoring
- Referenced by: Sales, InventoryLogs, and LowStockAlerts tables

#### Sales Table
```sql
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price FLOAT NOT NULL,
    total_amount FLOAT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_sales_product_date (product_id, sale_date),
    INDEX idx_sales_date_amount (sale_date, total_amount)
);
```
**Purpose**: Records all sales transactions
- Tracks individual sales with quantity and pricing information
- Maintains relationship with products through foreign key
- Optimized for date-range queries and product-specific sales analysis
- Used for: Sales analytics, revenue reporting, and inventory tracking

#### Inventory Logs Table
```sql
CREATE TABLE inventory_logs (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    change_type VARCHAR NOT NULL,  -- (purchase, sale, adjustment, return)
    quantity_change INTEGER NOT NULL,  -- Positive for additions, negative for reductions
    previous_quantity INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    notes VARCHAR,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_inventory_product_timestamp (product_id, timestamp),
    INDEX idx_inventory_type_timestamp (change_type, timestamp)
);
```
**Purpose**: Audit trail for inventory changes
- Records every stock level change with before/after quantities
- Tracks different types of inventory modifications
- Maintains complete history for auditing and analysis
- Used for: Inventory tracking, stock reconciliation, and audit trails

#### Low Stock Alerts Table
```sql
CREATE TABLE low_stock_alerts (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) UNIQUE,
    threshold INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_active_alerts (is_active, product_id)
);
```
**Purpose**: Manages inventory alert thresholds
- Configures product-specific stock level warnings
- One alert configuration per product (unique constraint)
- Supports active/inactive alert states
- Used for: Inventory management and restock notifications

### Entity Relationships

1. **Product to Sales** (One-to-Many)
   - One product can have multiple sales records
   - Each sale belongs to exactly one product
   - Relationship enforced by `product_id` foreign key in Sales table

2. **Product to Inventory Logs** (One-to-Many)
   - One product can have multiple inventory log entries
   - Each inventory log entry belongs to exactly one product
   - Tracks complete inventory history for each product

3. **Product to Low Stock Alert** (One-to-One)
   - Each product can have one low stock alert configuration
   - Enforced by unique constraint on `product_id` in Low Stock Alerts table

### Database Design Principles

1. **Normalization**
   - Tables are in Third Normal Form (3NF)
   - No redundant data storage
   - Each table has a clear, single purpose

2. **Referential Integrity**
   - Foreign key constraints ensure data consistency
   - Cascading updates/deletes configured where appropriate
   - No orphaned records possible

3. **Performance Optimization**
   - Strategic indexes on frequently queried columns
   - Composite indexes for common query patterns
   - Timestamp fields for temporal queries

4. **Audit Trail**
   - All tables include creation timestamps
   - Modified data includes update timestamps
   - Complete inventory change history maintained

### Query Optimization

The schema includes the following optimized query patterns:

1. **Product Queries**
   - Category-based filtering: `idx_product_category_stock`
   - Name search with category filter: `idx_product_name_category`

2. **Sales Analysis**
   - Date range queries: `idx_sales_date_amount`
   - Product-specific sales: `idx_sales_product_date`

3. **Inventory Tracking**
   - Product history: `idx_inventory_product_timestamp`
   - Change type analysis: `idx_inventory_type_timestamp`

4. **Alert Monitoring**
   - Active alerts: `idx_active_alerts`

## Usage Examples

### Adding Products

You can add products using either the REST API or GraphQL interface.

#### Using REST API

```bash
# Add a new product using cURL
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Gaming Mouse",
    "category": "Electronics",
    "price": 59.99,
    "stock": 100
  }'
```

Expected Response:
```json
{
  "id": 13,
  "name": "Wireless Gaming Mouse",
  "category": "Electronics",
  "price": 59.99,
  "stock": 100,
  "created_at": "2024-02-20T10:30:00",
  "updated_at": "2024-02-20T10:30:00"
}
```

#### Using GraphQL

You can use the GraphQL Playground at `http://localhost:8000/graphql` with this mutation:

```graphql
mutation CreateProduct {
  createProduct(input: {
    name: "Wireless Gaming Mouse"
    category: "Electronics"
    price: 59.99
    stock: 100
  }) {
    id
    name
    category
    price
    stock
    created_at
  }
}
```

Expected Response:
```json
{
  "data": {
    "createProduct": {
      "id": 13,
      "name": "Wireless Gaming Mouse",
      "category": "Electronics",
      "price": 59.99,
      "stock": 100,
      "created_at": "2024-02-20T10:30:00"
    }
  }
}
```

#### Product Fields

| Field    | Type    | Required | Description                    |
|----------|---------|----------|--------------------------------|
| name     | string  | Yes      | Product name                   |
| category | string  | Yes      | Product category               |
| price    | float   | Yes      | Product price (must be > 0)    |
| stock    | integer | Yes      | Initial stock quantity (≥ 0)   |

#### Available Categories
- Electronics
- Home & Kitchen
- Fashion
- Books
- Sports & Outdoors
- Beauty & Personal Care
- Toys & Games
- Grocery

#### Error Handling

The API will return appropriate error messages for:
- Missing required fields
- Invalid price (must be positive)
- Invalid stock quantity (must be non-negative)
- Invalid category

Example error response:
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "Price must be greater than 0",
      "type": "value_error"
    }
  ]
}
```
