from app.config.ai_config import ai_client
import json
from app.models.schemas import ProductFilters

def clean_llm_json(raw_response: str):
    # Remove markdown wrapper if present
    if raw_response.startswith('```json'):
        raw_response = raw_response[7:]
    if raw_response.endswith('```'):
        raw_response = raw_response[:-3]
    
    # Remove any explanations after the JSON
    raw_response = raw_response.strip()
    
    # Find the first { and last } to extract just the JSON
    first_brace = raw_response.find('{')
    last_brace = raw_response.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_str = raw_response[first_brace:last_brace + 1]
        return json.loads(json_str)
    
    raise ValueError("No valid JSON found in response")

def llm_call(prompt: str, temperature: float = 0.0) -> str:
    """Simple LLM call function using the configured AI client."""
    response = ai_client.chat.completions.create(
        model="dolphin-x1-8b",   # replace with your model name in LLM Studio
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    
    raw_content = response.choices[0].message.content.strip()
    clean_filters = clean_llm_json(raw_content)
    # print("Raw content:", raw_content, clean_filters)
    return clean_filters



def llm_to_filter(user_query: str) -> ProductFilters:
    prompt = f"""You are a precise Data Extraction Engine. Transform natural language queries into a JSON Filter Schema. Convert this user query to JSON filters.

    Schema: {{
    "name": {{"contains": ["string"]}},
    "description": {{"contains": ["string"]}}, 
    "quantity": {{"lt": number, "gt": number}},
    "price": {{"lt": number, "gt": number}}
    }}

    Rules:
    - Include misspellings AND correct spellings in contains arrays
    - Put same keywords in both name.contains and description.contains
    - Use lt for "under/less", gt for "over/more"
    - Omit fields not mentioned
    - Return ONLY JSON, no markdown

    Examples:
    Query: "cheap iphne under 500"
    Output: {{"name": {{"contains": ["cheap", "iphone", "iphne"]}}, "description": {{"contains": ["cheap", "iphone", "iphne"]}}, "price": {{"lt": 500}}}}

    Query: "{user_query}"

    Return ONLY JSON with the schema provided above. No explaination.
    """
    
    content = llm_call(prompt, temperature=0.0)
    return ProductFilters.model_validate(content)