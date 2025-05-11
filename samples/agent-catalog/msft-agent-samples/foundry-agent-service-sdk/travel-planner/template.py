import os
import jsonref
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    OpenApiTool,
    OpenApiConnectionAuthDetails,
    OpenApiConnectionSecurityScheme,
    BingGroundingTool,
    ToolSet,
    FunctionTool
)
from dotenv import load_dotenv

load_dotenv()

# Initialize the Agents client
agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Define a simple function tool
def get_travel_info():
    """Get basic travel information."""
    return "I can help you plan your trip!"

# [START create_agent_with_toolset]
# Initialize Bing tool
bing_tool = BingGroundingTool(connection_id=os.environ["BING_CONNECTION_ID"])

# Load OpenAPI spec
with open("tripadvisor.openapi.json", "r") as f:
    spec = jsonref.loads(f.read())

# Create TripAdvisor tool
tripadvisor_tool = OpenApiTool(
    name="TripAdvisorAPI",
    description="Access TripAdvisor location details, photos, and reviews via OpenAPI.",
    spec=spec,
    auth=OpenApiConnectionAuthDetails(
        security_scheme=OpenApiConnectionSecurityScheme(
            connection_id=os.environ["TRIPADVISOR_CONNECTION_ID"]
        )
    )
)

# Initialize toolset and add tools
toolset = ToolSet()
toolset.add(bing_tool)
toolset.add(tripadvisor_tool)
toolset.add(FunctionTool([get_travel_info]))  # Add FunctionTool

# Create the agent using the toolset
with agents_client:
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="travel-planner-agent",
        instructions="""
You are a trustworthy and knowledgeable travel assistant.
Use Tripadvisor to recommend destinations, attractions, hotels, restaurants, and experiences based on verified traveler reviews, popularity, and relevance.
Use Bing to provide up-to-date information such as weather forecasts, travel advisories, local events, business hours, and transportation options.

Always:
- Tailor recommendations to the user's stated preferences, such as budget, trip duration, dietary needs, or mobility concerns.
- Verify time-sensitive information (e.g., availability, closures, visa rules) using Bing before presenting it.
- Highlight both pros and cons when summarizing reviews or comparisons.
- Prioritize safety, accessibility, and cultural sensitivity in all suggestions.

Never:
- Provide medical, legal, or visa advice beyond publicly available information.
- Generate or speculate about reviews, ratings, or availability not sourced from Tripadvisor or Bing.
- Promote or prioritize businesses or services without a clear basis in user need, review data, or trusted search results.
- Encourage or assist in activities that are illegal, unsafe, or violate the terms of Tripadvisor, Bing, or local laws.

When unsure, clearly state limitations and recommend that the user verify critical details directly with official sources.
        """,
        toolset=toolset
    )
    print(f"✅ Agent created: {agent.id}")
