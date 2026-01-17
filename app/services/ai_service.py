from app.utils.ai_utils import llm_call, llm_to_filter


def get_ai_product_filters(user_query: str):
    """Get AI-generated product filters from natural language query."""
    return llm_to_filter(user_query)