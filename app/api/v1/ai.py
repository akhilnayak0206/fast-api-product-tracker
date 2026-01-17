from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.ai_service import get_ai_product_filters
from app.repositories.product_repository import ProductRepository
from app.core.database import get_db
from app.models.schemas import ProductResponse, ProductListResponse, ProductQuery
from app.utils.ai_utils import llm_call

router = APIRouter()


@router.post("/debug/llm-filter")
async def debug_ai_product_filters(user_query: str):
    """Debug endpoint to test AI-generated product filters from natural language."""
    ai_response = get_ai_product_filters(user_query)
    return {"ai_response": ai_response}


@router.post("/product-search", response_model=ProductListResponse)
async def search_products_with_ai(
    query: ProductQuery,
    db: Session = Depends(get_db)
):
    """Search products using AI-generated filters from natural language query."""
    try:
        # Generate filters using AI
        ai_filters = get_ai_product_filters(query.user_query)
        
        # Create repository and search with filters
        product_repo = ProductRepository(db)
        products = product_repo.get_with_filters(ai_filters)
        
        # Convert to response format
        product_responses = [ProductResponse.model_validate(product) for product in products]
        
        return ProductListResponse(
            products=product_responses,
            count=len(product_responses)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")
