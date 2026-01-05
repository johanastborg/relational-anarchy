import logging
import os
from src.db.rdbms import MockRDBMS
from src.db.spanner import SpannerGraphClient
from src.llm.gemini_client import GeminiClient
from src.agents.extractor import ExtractorAgent
from src.agents.loader import LoaderAgent
from src.swarm import SwarmOrchestrator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    # Configuration (In a real app, load from env vars or config file)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "mock-project")
    INSTANCE_ID = os.getenv("SPANNER_INSTANCE", "mock-instance")
    DATABASE_ID = os.getenv("SPANNER_DATABASE", "mock-db")
    GRAPH_NAME = os.getenv("SPANNER_GRAPH", "MyGraph")

    logging.info("Initializing Agentic Swarm...")

    # 1. Initialize Infrastructure Clients
    # Using MockRDBMS for demonstration. Replace with real implementation for production.
    rdbms = MockRDBMS()

    spanner_client = SpannerGraphClient(INSTANCE_ID, DATABASE_ID, PROJECT_ID)

    gemini_client = GeminiClient(PROJECT_ID)

    # 2. Initialize Agents
    extractor = ExtractorAgent(gemini_client)
    loader = LoaderAgent(spanner_client, GRAPH_NAME)

    # 3. Initialize Orchestrator
    swarm = SwarmOrchestrator(rdbms, extractor, loader)

    # 4. Run
    swarm.run()

if __name__ == "__main__":
    main()
