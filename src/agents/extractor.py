from typing import List, Dict, Any
from src.agents.base import Agent
from src.llm.gemini_client import GeminiClient

class ExtractorAgent(Agent):
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("ExtractorAgent")
        self.llm = gemini_client

    def run(self, schema: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes table schema and data, and asks LLM to convert it to graph nodes and edges.
        """
        self.log(f"Processing {len(data)} rows.")

        prompt = f"""
        You are a knowledge graph expert. I have relational data that I want to convert into a graph structure.

        Table Schema:
        {schema}

        Data Rows:
        {data}

        Please identify the entities (nodes) and relationships (edges) in this data.

        Return a JSON object with two keys: "nodes" and "edges".

        "nodes" should be a list of objects with "id", "label", and "properties".
        "edges" should be a list of objects with "source", "target", "label", and "properties".

        Ensure that foreign keys are treated as edges between entities.
        """

        result = self.llm.generate_json(prompt)
        self.log(f"Extracted {len(result.get('nodes', []))} nodes and {len(result.get('edges', []))} edges.")
        return result
