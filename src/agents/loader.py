from typing import Dict, Any
from src.agents.base import Agent
from src.db.spanner import SpannerGraphClient

class LoaderAgent(Agent):
    def __init__(self, spanner_client: SpannerGraphClient, graph_name: str):
        super().__init__("LoaderAgent")
        self.spanner = spanner_client
        self.graph_name = graph_name

    def run(self, graph_data: Dict[str, Any]):
        """
        Takes graph data (nodes/edges) and loads them into Spanner.
        """
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])

        self.log(f"Loading {len(nodes)} nodes and {len(edges)} edges into graph '{self.graph_name}'.")

        if nodes:
            self.spanner.insert_vertices(self.graph_name, nodes)

        if edges:
            self.spanner.insert_edges(self.graph_name, edges)

        self.log("Load complete.")
