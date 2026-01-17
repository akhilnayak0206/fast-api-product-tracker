from app.config.ai_config import ai_client
import json
from app.models.schemas import ProductFilters


def llm_call(prompt: str, temperature: float = 0.0):
    """Simple LLM call function using the configured AI client."""
    response = ai_client.chat.completions.create(
        model="dolphin-x1-8b",   # replace with your model name in LLM Studio
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()



def llm_to_filter(user_query: str) -> ProductFilters:
    prompt = f"""
                You are an API that converts natural language into product filters.
                Return ONLY valid JSON.

                Schema:
                {{
                "name": {{"contains": [string]}},
                "description": {{"contains": [string]}},
                "quantity": {{"lt": number, "gt": number}},
                "price": {{"lt": number, "gt": number}}
                }}

                Rules:
                - If user mentions product name similarity, use name.contains with array of relevant terms
                - If user mentions description/meaning/related/like/similar, use description.contains with array of relevant terms
                - If user mentions quantity, use quantity.lt and/or quantity.gt
                - If user mentions price, use price.lt and/or price.gt
                - If unsure about name or description add them in both fields
                - If something is not mentioned, omit it
                - Do not add any extra keys
                - Do not add explanations


                User: {user_query}
            """
    content = llm_call(prompt, temperature=0.0)
    return ProductFilters.model_validate(json.loads(content))