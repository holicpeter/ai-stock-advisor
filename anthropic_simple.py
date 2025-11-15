import httpx
import json

class AnthropicClient:
    """Simple Anthropic API client without using their SDK"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    
    def create_message(self, model, max_tokens, system, messages):
        """Create a message using Anthropic API"""
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages
        }
        
        response = httpx.post(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=30.0
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        
        result = response.json()
        
        # Create response object similar to anthropic SDK
        class Response:
            def __init__(self, data):
                self.content = [type('obj', (object,), {'text': data['content'][0]['text']})]
                self.usage = type('obj', (object,), {
                    'input_tokens': data['usage']['input_tokens'],
                    'output_tokens': data['usage']['output_tokens']
                })
        
        return Response(result)
