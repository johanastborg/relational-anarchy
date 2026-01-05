from typing import List
from src.db.rdbms import RDBMSInterface
from src.agents.extractor import ExtractorAgent
from src.agents.loader import LoaderAgent
import logging

logger = logging.getLogger(__name__)

class SwarmOrchestrator:
    def __init__(self,
                 rdbms: RDBMSInterface,
                 extractor: ExtractorAgent,
                 loader: LoaderAgent):
        self.rdbms = rdbms
        self.extractor = extractor
        self.loader = loader

    def run(self, tables: List[str] = None):
        """
        Main loop:
        1. Identify tables to process.
        2. Fetch data from RDBMS.
        3. Pass to ExtractorAgent (LLM) to get Graph structure.
        4. Pass to LoaderAgent to write to Spanner.
        """
        if tables is None:
            tables = self.rdbms.list_tables()

        logger.info(f"Starting swarm for tables: {tables}")

        for table in tables:
            logger.info(f"Processing table: {table}")

            # Step 1: Get Schema and Data
            schema = self.rdbms.fetch_table_schema(table)
            data = self.rdbms.fetch_data(table)

            if not data:
                logger.warning(f"No data found for table {table}")
                continue

            # Step 2: Extract Graph Structure
            # We might chunk data here if it's large, but for this basic structure we take the batch.
            graph_data = self.extractor.run(schema, data)

            # Step 3: Load into Spanner
            self.loader.run(graph_data)

        logger.info("Swarm execution finished.")
