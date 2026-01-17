from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class ProductFilter(BaseModel):
    """Schema for AI-generated product filters"""
    contains: Optional[List[str]] = None


class NumericFilter(BaseModel):
    """Schema for numeric range filters"""
    lt: Optional[float] = None
    gt: Optional[float] = None


class ProductFilters(BaseModel):
    """Schema for all product filters"""
    name: Optional[ProductFilter] = None
    description: Optional[ProductFilter] = None
    quantity: Optional[NumericFilter] = None
    price: Optional[NumericFilter] = None


class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    quantity: int


class ProductCreate(ProductBase):
    """Schema for creating products - ID is auto-generated"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating products - all fields optional"""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    quantity: Optional[int] = None


class ProductResponse(ProductBase):
    """Schema for product responses - includes UUID"""
    id: UUID
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    count: int


class ErrorResponse(BaseModel):
    error: str
    message: str
