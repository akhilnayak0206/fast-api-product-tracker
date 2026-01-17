
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import session, engine
from models import Product
import database_models
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(
    title="Product Tracker API",
    description="A simple API for managing products",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the frontend to make requests to this API from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create all database tables based on the models defined in database_models
# This ensures the database schema matches our model definitions
database_models.Base.metadata.create_all(bind=engine)

# Sample products for initial database seeding
# These will be added to the database when the application starts
products = [
    Product(id=1, name="Product 1", price=10.0, description="Description 1", quantity=10),
    Product(id=2, name="Product 2", price=20.0, description="Description 2", quantity=20),
    Product(id=3, name="Product 3", price=30.0, description="Description 3", quantity=30)
]

def get_db():
    """
    Database dependency function
    
    This function provides a database session to our API endpoints.
    It ensures that the database connection is properly closed after each request.
    
    Yields:
        Session: Database session for the current request
    """
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database with sample data
    
    This function checks if the database is empty and adds sample products
    if no products exist. This prevents duplicate data on app restart.
    """
    db = session()

    # Check if products already exist in the database
    count = db.query(database_models.Product).count()
    if count > 0:
        return  # Database already has data, skip initialization
    
    # Add sample products to the database
    for product in products:
        db.add(database_models.Product(**product.model_dump()))
    db.commit()

# Initialize the database when the application starts
init_db()

@app.get("/")
def greet():
    """
    Root endpoint
    
    Returns a simple greeting message to confirm the API is running.
    
    Returns:
        str: Hello message
    """
    return "Hello, World!"

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    """
    Get all products endpoint
    
    Retrieves all products from the database.
    
    Args:
        db (Session): Database session dependency
        
    Returns:
        List[Product]: List of all products in the database
    """
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID endpoint
    
    Retrieves a single product from the database using its ID.
    
    Args:
        id (int): The ID of the product to retrieve
        db (Session): Database session dependency
        
    Returns:
        Product: The requested product if found
        str: Error message if product not found
    """
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        return db_product
    return "Product not found"

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    """
    Create a new product endpoint
    
    Adds a new product to the database.
    
    Args:
        product (Product): The product data to create
        db (Session): Database session dependency
        
    Returns:
        Product: The created product data
    """
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    """
    Update a product endpoint
    
    Updates an existing product in the database.
    Only updates fields that are provided (not None).
    
    Args:
        id (int): The ID of the product to update
        product (Product): The updated product data
        db (Session): Database session dependency
        
    Returns:
        str: Success message if updated
        str: Error message if product not found
    """
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        # Only update fields that are not None (allows partial updates)
        if product.name is not None:
            db_product.name = product.name
        if product.price is not None:
            db_product.price = product.price
        if product.description is not None:
            db_product.description = product.description
        if product.quantity is not None:
            db_product.quantity = product.quantity
        db.commit()
        return "Product updated"
    return "Product not found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Delete a product endpoint
    
    Removes a product from the database using its ID.
    
    Args:
        id (int): The ID of the product to delete
        db (Session): Database session dependency
        
    Returns:
        str: Success message if deleted
        str: Error message if product not found
    """
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    return "Product not found"