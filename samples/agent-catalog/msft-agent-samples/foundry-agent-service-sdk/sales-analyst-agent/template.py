from azure.ai.agent import Agent, Tool, CodeInterpreterTool, FileSearchTool
from azure.ai.agent.runtime import AgentRuntime
from azure.ai.agent.models import ToolDefinition

# Agent system message
SYSTEM_MESSAGE = """You are an expert sales analyst.
Use the uploaded sales data to answer questions about orders, customers, regions, and product performance.
Always explain your reasoning and cite relevant files or calculations."""

# Initialize tools
file_search_tool = FileSearchTool(name="file_search", vector_store_ids=["<your-vector-store-id>"])
code_interpreter_tool = CodeInterpreterTool(name="code_interpreter")

tools = [file_search_tool, code_interpreter_tool]

# Define the agent
agent = Agent(
    name="sales-analyst-agent",
    instructions=SYSTEM_MESSAGE,
    tools=[ToolDefinition.from_tool(t) for t in tools],
)

# Optional: agent runtime for programmatic execution
runtime = AgentRuntime(agent=agent)

if __name__ == "__main__":
    print("Sales Analyst Agent template loaded successfully.")
