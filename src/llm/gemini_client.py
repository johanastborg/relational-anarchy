import vertexai
from vertexai.generative_models import GenerativeModel, Part
import logging
import os
import json

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, project_id: str, location: str = "us-central1", model_name: str = "gemini-1.5-flash-001"):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.model = None
        self._initialized = False
        # Force mock mode if explicitly requested or if we suspect no creds (could add check here)
        self.mock_mode = os.getenv("USE_MOCK_LLM", "false").lower() == "true"

    def _initialize(self):
        if not self._initialized and not self.mock_mode:
            try:
                vertexai.init(project=self.project_id, location=self.location)
                self.model = GenerativeModel(self.model_name)
                self._initialized = True
            except Exception as e:
                logger.warning(f"Failed to initialize Vertex AI: {e}. Switching to Mock mode.")
                self.mock_mode = True

    def generate_content(self, prompt: str) -> str:
        self._initialize()

        if not self.mock_mode and self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating content: {e}. Falling back to mock response.")
                # If we fail during generation (e.g. auth error), fallback to mock
                return self._mock_response(prompt)
        else:
            return self._mock_response(prompt)

    def generate_json(self, prompt: str) -> dict:
        """
        Helper to ensure we get JSON back.
        """
        full_prompt = f"{prompt}\n\nOutput the result strictly as a valid JSON object."
        response_text = self.generate_content(full_prompt)

        # Basic cleanup to handle markdown code blocks
        clean_text = response_text.replace("```json", "").replace("```", "").strip()

        if not clean_text:
             return {}

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response_text}")
            return {}

    def _mock_response(self, prompt: str) -> str:
        """
        Returns a mock response based on keywords in the prompt.
        """
        logger.info("Generating mock response")
        if "users" in prompt:
            return json.dumps({
                "nodes": [
                    {"id": "1", "label": "User", "properties": {"name": "Alice", "role": "admin"}},
                    {"id": "2", "label": "User", "properties": {"name": "Bob", "role": "user"}},
                    {"id": "3", "label": "User", "properties": {"name": "Charlie", "role": "user"}}
                ],
                "edges": []
            })
        elif "orders" in prompt:
            return json.dumps({
                "nodes": [
                    {"id": "101", "label": "Order", "properties": {"product": "Laptop", "amount": 1200}},
                    {"id": "102", "label": "Order", "properties": {"product": "Phone", "amount": 800}},
                    {"id": "103", "label": "Order", "properties": {"product": "Monitor", "amount": 300}}
                ],
                "edges": [
                    {"source": "1", "target": "101", "label": "PLACED", "properties": {}},
                    {"source": "2", "target": "102", "label": "PLACED", "properties": {}},
                    {"source": "1", "target": "103", "label": "PLACED", "properties": {}}
                ]
            })
        return "{}"
