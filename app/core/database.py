from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import settings
from app.models import Base, Product

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    Database dependency function
    
    This function provides a database session to our API endpoints.
    It ensures that the database connection is properly closed after each request.
    
    Yields:
        Session: Database session for the current request
    """
    db = SessionLocal()
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
    db = SessionLocal()
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Check if products already exist in the database
        count = db.query(Product).count()
        if count > 0:
            return  # Database already has data, skip initialization
        
        # Add sample products to the database (without IDs - auto-generated UUIDs)
        from app.models.schemas import ProductCreate
        sample_products = [
            ProductCreate(name="Product 1", price=10.0, description="Description 1", quantity=10),
            ProductCreate(name="Product 2", price=20.0, description="Description 2", quantity=20),
            ProductCreate(name="Product 3", price=30.0, description="Description 3", quantity=30)
        ]
        
        for product_data in sample_products:
            db_product = Product(**product_data.model_dump())
            db.add(db_product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
