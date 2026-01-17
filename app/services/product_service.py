from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
import database_models
from uuid import UUID


class ProductService:
    """Service layer for product business logic"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def get_all_products(self) -> ProductListResponse:
        """Get all products with count"""
        products = self.repository.get_all()
        product_responses = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=product_responses, count=len(product_responses))
    
    def get_product_by_id(self, product_id: UUID) -> Optional[ProductResponse]:
        """Get a specific product by UUID"""
        product = self.repository.get_by_id(product_id)
        if product:
            return ProductResponse.model_validate(product)
        return None
    
    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product"""
        product = self.repository.create(product_data)
        return ProductResponse.model_validate(product)
    
    def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Optional[ProductResponse]:
        """Update an existing product"""
        product = self.repository.update(product_id, product_data)
        if product:
            return ProductResponse.model_validate(product)
        return None
    
    def delete_product(self, product_id: UUID) -> bool:
        """Delete a product"""
        return self.repository.delete(product_id)
    
    def product_exists(self, product_id: UUID) -> bool:
        """Check if a product exists"""
        return self.repository.get_by_id(product_id) is not None
