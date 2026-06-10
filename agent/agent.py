import os
import logging
from dotenv import load_dotenv
from google.adk import Runner
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reporting-agent")

load_dotenv()

# Force environment variables for Vertex AI to override Cloud Shell defaults
os.environ["GOOGLE_CLOUD_PROJECT"] = "dh-imd"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

# Constants for Folder IDs
INPUT_BASE_FOLDER_ID = "1ViJRMx8dd8tZ9S6n1P5Luw_ifx8tcwnR"
OUTPUT_FOLDER_ID = "1agqVvkOnwTZkUhVZHeJDZOFv_h_UZJrk"

SYSTEM_INSTRUCTION = """
You are a Senior Business Reporting Analyst. Your goal is to generate a concise monthly report based ONLY on the content of the files provided to you.

STRICT GROUNDING RULES:
1. ONLY use information explicitly stated in the provided files.
2. DO NOT hallucinate, guess, or use external knowledge to fill in gaps.
3. If information for a specific segment (e.g., Financial performance) is missing from the files, state "Data not provided in the source files."
4. Be extremely concise. Use a maximum of 3 short bullet points per segment.

PROCESS:
1. Review the text and visual content from the uploaded files.
2. Extract and synthesize data for each brand.
3. Generate the report using the following structured format:

# [Brand Name]

## 📊 Summary
### Top 3 highlights
* [Factual Highlight 1]
* [Factual Highlight 2]
* [Factual Highlight 3]

### Top 3 Lowlights
* [Factual Lowlight 1]
* [Factual Lowlight 2]
* [Factual Lowlight 3]

## 💬 Discussion points
* [Point 1]
* [Point 2]
* [Point 3]

## 💰 Financial performance
* [Factual Metric 1]
* [Factual Metric 2]
* [Factual Metric 3]

## ⚙️ Operational performance
* [Factual Metric 1]
* [Factual Metric 2]
* [Factual Metric 3]

## 🌟 Special Topics
* [Note 1]
* [Note 2]
* [Note 3]

4. If a brand has no data or a meeting is cancelled, output "# [Brand Name]\n\n**Meeting cancelled.**"
5. Return the final report as a single Markdown-formatted string.
gemini"""

agent = LlmAgent(
    name="reporting_analyst",
    model="gemini-2.5-flash",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ]
)

if __name__ == "__main__":
    # In the new frontend workflow, the frontend would pass the text of the files
    # directly in the prompt or use tool calls if the files are on Drive.
    example_query = "Here is the content from the February slides: [Slide Content...]. Please generate the report."
    
    # Initialize Runner
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, session_service=session_service, app_name="reporting_app", auto_create_session=True)
    
    print(f"--- 🚀 Agent Ready for Frontend Integration ---")
