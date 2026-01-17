from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.product_service import ProductService
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from uuid import UUID

class BaseProductRouter:
    """Base router with common product functionality"""
    
    def __init__(self):
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup common routes - can be overridden in subclasses"""
        self.router.add_api_route(
            "/", 
            self.get_all_products, 
            methods=["GET"], 
            response_model=ProductListResponse
        )
        self.router.add_api_route(
            "/{product_id}", 
            self.get_product_by_id, 
            methods=["GET"], 
            response_model=ProductResponse
        )
        self.router.add_api_route(
            "/", 
            self.create_product, 
            methods=["POST"], 
            response_model=ProductResponse,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{product_id}", 
            self.update_product, 
            methods=["PUT"], 
            response_model=ProductResponse
        )
        self.router.add_api_route(
            "/{product_id}", 
            self.delete_product, 
            methods=["DELETE"], 
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    async def get_all_products(self, db: Session = Depends(get_db)):
        """Get all products - can be overridden for version-specific behavior"""
        try:
            service = ProductService(db)
            return service.get_all_products()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving products: {str(e)}"
            )
    
    async def get_product_by_id(self, product_id: UUID, db: Session = Depends(get_db)):
        """Get product by UUID - can be overridden for version-specific behavior"""
        try:
            service = ProductService(db)
            product = service.get_product_by_id(product_id)
            if product:
                return product
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving product: {str(e)}"
            )
    
    async def create_product(self, product: ProductCreate, db: Session = Depends(get_db)):
        """Create product - can be overridden for version-specific validation"""
        try:
            service = ProductService(db)
            return service.create_product(product)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating product: {str(e)}"
            )
    
    async def update_product(self, product_id: UUID, product: ProductUpdate, db: Session = Depends(get_db)):
        """Update product - can be overridden for version-specific behavior"""
        try:
            service = ProductService(db)
            updated_product = service.update_product(product_id, product)
            if updated_product:
                return updated_product
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating product: {str(e)}"
            )
    
    async def delete_product(self, product_id: UUID, db: Session = Depends(get_db)):
        """Delete product - can be overridden for version-specific behavior"""
        try:
            service = ProductService(db)
            success = service.delete_product(product_id)
            if success:
                return
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting product: {str(e)}"
            )
