from app.utils.ai_utils import AIUtils

ai_utils = AIUtils()

def get_ai_product_filters(user_query: str):
    """Get AI-generated product filters from natural language query."""
    try:
        return ai_utils.llm_to_filter(user_query)
    except Exception as e:
        # Re-raise with more context about the service layer
        raise Exception(f"Failed to generate AI product filters for query '{user_query}': {str(e)}")
