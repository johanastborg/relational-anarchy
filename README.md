# Agentic Swarm for RDBMS to Spanner Graph

This project implements a basic agentic swarm structure to convert relational data into a knowledge graph stored in Google Cloud Spanner Graph.

## Architecture

The system consists of three main components:

1.  **Agents**:
    *   `ExtractorAgent`: Uses Google Gemini (via Vertex AI) to analyze relational table schemas and data, extracting entities (nodes) and relationships (edges).
    *   `LoaderAgent`: Takes the extracted graph structure and loads it into Google Cloud Spanner Graph.
2.  **Orchestrator**:
    *   `SwarmOrchestrator`: Coordinates the workflow, iterating through tables and managing the data flow between agents.
3.  **Infrastructure**:
    *   `RDBMSInterface`: Abstract interface for reading relational data. A `MockRDBMS` is provided for demonstration.
    *   `SpannerGraphClient`: Interface for interacting with Spanner Graph.
    *   `GeminiClient`: Interface for interacting with Vertex AI / Gemini models.

## Prerequisites

*   Python 3.8+
*   Google Cloud Project with Vertex AI and Spanner API enabled.
*   Application Default Credentials (ADC) configured.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Set the following environment variables (optional, defaults are provided for testing):

*   `GOOGLE_CLOUD_PROJECT`: Your GCP Project ID.
*   `SPANNER_INSTANCE`: Spanner Instance ID.
*   `SPANNER_DATABASE`: Spanner Database ID.
*   `SPANNER_GRAPH`: Name of the Graph in Spanner.

## Running the Swarm

To run the application:

```bash
export PYTHONPATH=$PYTHONPATH:.
python src/main.py
```

## Testing / Mock Mode

If you do not have active GCP credentials, the `GeminiClient` will automatically fallback to a "Mock Mode", returning predefined responses for the sample `users` and `orders` data. This allows you to verify the logic flow without incurring costs or needing immediate access.
