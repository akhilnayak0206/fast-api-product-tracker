from app.config.ai_config import ai_client
import json
from app.models.schemas import ProductFilters

class AIUtils:
    def __init__(self, client=ai_client, model="openai/gpt-oss-120b"):
        self.client = client
        self.model = model

    def clean_llm_json(self, raw_response: str):
        # Work with a copy to avoid modifying the original argument
        response = raw_response
        
        # Remove markdown wrapper if present
        if response.startswith('```json'):
            response = response[7:]
        if response.endswith('```'):
            response = response[:-3]
        
        # Remove any explanations after the JSON
        response = response.strip()
        
        # Find all JSON objects in the response
        json_objects = []
        start = 0
        
        while True:
            first_brace = response.find('{', start)
            if first_brace == -1:
                break
                
            # Find matching closing brace
            brace_count = 0
            last_brace = -1
            
            for i in range(first_brace, len(response)):
                if response[i] == '{':
                    brace_count += 1
                elif response[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_brace = i
                        break
            
            if last_brace != -1 and last_brace > first_brace:
                json_str = response[first_brace:last_brace + 1]
                try:
                    json_obj = json.loads(json_str)
                    json_objects.append(json_obj)
                except json.JSONDecodeError:
                    pass  # Skip invalid JSON
                start = last_brace + 1
            else:
                break
        
        if not json_objects:
            print(f"Raw AI response with no valid JSON: {raw_response}")
            raise ValueError("No valid JSON found in response")
        
        # Merge all JSON objects
        merged_result = {}
        for obj in json_objects:
            merged_result.update(obj)
        
        return merged_result

    def llm_call(self, prompt: str, temperature: float = 0.0) -> str:
        """Simple LLM call function using the configured AI client."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            
            if not response.choices or not response.choices[0].message:
                raise ValueError("Empty response from AI model")
                
            raw_content = response.choices[0].message.content.strip()
            if not raw_content:
                raise ValueError("Empty content in AI response")
                
            # print("Raw content:", raw_content,"\n\n")
            clean_filters = self.clean_llm_json(raw_content)
            # print("Raw content:", raw_content, clean_filters,"\n\n")
            return clean_filters
            
        except Exception as e:
            # Handle different types of errors appropriately
            error_msg = f"AI LLM call failed: {str(e)}"
            if "openai" in str(type(e)).lower() or "api" in str(e).lower():
                # OpenAI API errors
                raise Exception(f"AI API error: {str(e)}")
            elif "connection" in str(e).lower():
                # Connection errors
                raise Exception(f"AI service connection error: {str(e)}")
            elif "timeout" in str(e).lower():
                # Timeout errors
                raise Exception(f"AI service timeout error: {str(e)}")
            elif "json" in str(e).lower():
                # JSON parsing errors
                raise Exception(f"AI response parsing error: {str(e)}")
            else:
                # General errors
                raise Exception(error_msg)

    def llm_to_filter(self, user_query: str) -> ProductFilters:
        prompt = f"""You are a precise Data Extraction Engine for e-commerce website. Transform natural language queries into a JSON Filter Schema. Convert this user query to JSON filters.

        Schema: {{
        "name": {{"contains": ["string"]}},
        "description": {{"contains": ["string"]}}, 
        "quantity": {{"lt": number, "gt": number}},
        "price": {{"lt": number, "gt": number}}
        }}

        Rules:
        - Include misspellings AND correct spellings in contains arrays
        - Put same keywords in both name.contains and description.contains
        - Create similar words for those keywords and include them as well in the contains arrays
        - Use lt for "under/less", gt for "over/more"
        - Omit fields not mentioned
        - Return ONLY JSON, no markdown

        Query: "{user_query}"

        Return ONLY JSON with the schema provided above. No explanation.
        """
        
        content = self.llm_call(prompt, temperature=0.0)
        return ProductFilters.model_validate(content)
