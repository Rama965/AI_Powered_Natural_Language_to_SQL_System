import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool,
)

from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.openai import OpenAILlmService

load_dotenv()


class DefaultUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="default_user",
            email="default_user@example.com",
            group_memberships=["admin", "user"],
        )


def create_agent() -> Agent:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is missing in your environment variables.")

    llm = OpenAILlmService(
        api_key=groq_api_key,
        model="llama-3.3-70b-versatile",
        base_url="https://api.groq.com/openai/v1",
    )

    tools = ToolRegistry()
    tools.register_local_tool(
        RunSqlTool(sql_runner=SqliteRunner(database_path="./clinic.db")),
        access_groups=["admin", "user"],
    )
    tools.register_local_tool(
        VisualizeDataTool(),
        access_groups=["admin", "user"],
    )
    tools.register_local_tool(
        SaveQuestionToolArgsTool(),
        access_groups=["admin"],
    )
    tools.register_local_tool(
        SearchSavedCorrectToolUsesTool(),
        access_groups=["admin", "user"],
    )

    agent_memory = DemoAgentMemory(max_items=1000)
    user_resolver = DefaultUserResolver()

    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=user_resolver,
        agent_memory=agent_memory,
        config=AgentConfig(),
    )

    return agent


agent = create_agent()