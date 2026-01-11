
# Product Inventory Management

A comprehensive product inventory management system built with FastAPI backend and React frontend, providing seamless tracking and management of product inventory.

## Features

- **GET /**: Welcome endpoint
- **GET /products/**: Get all products
- **GET /products/{product_id}**: Get a specific product by ID
- **POST /products/**: Create a new product
- **PUT /products/{product_id}**: Update a product
- **DELETE /products/{product_id}**: Delete a product

## Setup

### Prerequisites

- Python 3.7+
- PostgreSQL database (or other supported database)

### 1. Clone the repository
```bash
git clone <repository-url>
cd product-tracker-fastapi
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### 4. Set up environment variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your database configuration
# DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 5. Set up the database
- Create a PostgreSQL database
- Update the `DATABASE_URL` in your `.env` file with your database credentials

### 6. Run the application
```bash
uvicorn main:app --reload
```

### 7. Access the API
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

The application uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `postgresql://username:password@localhost:5432/db_name` |

## Database Support

This application supports multiple database backends:

- **PostgreSQL** (recommended for production)
- **SQLite** (for development)
- **MySQL**
- Any other SQLAlchemy-supported database

Example database URLs:
```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database_name

# SQLite
DATABASE_URL=sqlite:///./products.db

# MySQL
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

## Project Structure

```
product-tracker-fastapi/
├── main.py              # FastAPI application with endpoints
├── models.py            # Pydantic models
├── database_models.py   # SQLAlchemy database models
├── database.py          # Database configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore file
├── frontend/            # React frontend application
└── README.md            # This file
```

## API Usage Examples

### Get all products
```bash
curl http://localhost:8000/products/
```

### Get product by ID
```bash
curl http://localhost:8000/products/1
```

### Create a new product
```bash
curl -X POST "http://localhost:8000/products/" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 5,
       "name": "Monitor",
       "description": "4K monitor",
       "price": 299.99,
       "quantity": 15
     }'
```

### Update a product
```bash
curl -X PUT "http://localhost:8000/products/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Monitor",
       "price": 349.99
     }'
```

### Delete a product
```bash
curl -X DELETE "http://localhost:8000/products/1"
```

## Screenshots

Here's a preview of the Product Tracker application:

![Product Tracker Screenshot](./screenshots/full_screen.png)

*Note: The screenshot is located in the screenshot folder.*

## Models

### Product
- `id`: integer
- `name`: string
- `description`: string
- `price`: float
- `quantity`: integer

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints
- [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

## Special Thanks

Thanks to Telusko

## Author

**Akhil Nayak**

ThankYou.Peace.

