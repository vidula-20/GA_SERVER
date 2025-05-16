from contextlib import AsyncExitStack
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from google.adk.agents.llm_agent import LlmAgent, Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


async def create_agent():
    common_exit_stack = AsyncExitStack()
    tools, _ = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url="http://localhost:8080/sse",
            # Optionally, add headers={"Authorization": "Bearer ..."} if needed
        ),
        async_exit_stack=common_exit_stack
    )


    agent = LlmAgent(
        model='gemini-2.5-flash-preview-04-17',
        name='analytics_assistant',
        instruction="""
You are an assistant that helps users with their Google Analytics 4 (GA4) queries.

You can use the provided MCP tools to answer questions about website and app analytics, including:
- Page views, most/least popular pages, and trends
- User and session metrics (active users, new users, sessions, engagement, retention)
- Events and conversions (event counts, conversion rates)
- Traffic sources and campaigns
- Devices, platforms, browsers, and operating systems
- Geography and user demographics
- E-commerce and product performance
- Custom dimensions and metrics
- Retention, cohort, and user lifetime value
- App-specific analytics

For each question:
- Select the most relevant tool from the list.
- Specify appropriate dimensions and metrics (such as page, product, date, source, device, etc.).
- If the question is about comparisons, trends, or rankings, use time-based or category-based breakdowns (e.g., add "date" or "pagePath" as a dimension).
- If the user’s request is unclear, ask clarifying questions.
- If the user asks for data outside the scope of these tools, explain what analytics you can provide and suggest the closest available report.



Always provide clear, concise, and actionable answers.
""",
        tools=tools,
    )
    return agent, common_exit_stack
    
root_agent = create_agent()
    
    # Now you can use `agent` as needed