# E-commerce Admin API

A FastAPI-based backend API for e-commerce admin dashboard with powerful analytics capabilities.

## Features

- Sales analytics and reporting
- Revenue analysis (daily, weekly, monthly, annual)
- Category-wise performance metrics
- Time-series data for sales trends
- Product inventory management

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database and create a `.env` file:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_admin
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Sales Analytics

- `POST /sales/` - Create a new sale record
- `GET /sales/analytics` - Get overall sales analytics
- `GET /sales/analytics/category` - Get category-wise sales analytics
- `GET /sales/analytics/timeline` - Get time-series sales data

### Query Parameters

Most analytics endpoints support the following query parameters:
- `start_date`: Start date for the analysis period (ISO format)
- `end_date`: End date for the analysis period (ISO format)
- `period`: For timeline analysis (daily/weekly/monthly/annual)
