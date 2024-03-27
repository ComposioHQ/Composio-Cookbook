#!pip install pyautogen composio_autogen --quiet

from autogen import AssistantAgent, UserProxyAgent
from composio_autogen import App, Action, ComposioToolset
import os

llm_config = {
    "config_list": [
        {
            "model": "gpt-4-turbo-preview",
            "api_key": os.environ.get("OPENAI_API_KEY", "sk-123***"),
        }
    ]
}

super_agent = AssistantAgent(
    "chatbot",
    system_message="""You are a super intelligent personal assistant.
    You have been given a set of tools that you are supposed to choose from.
    You decide the right tool and execute it to achieve your task.
    Reply TERMINATE when the task is done or when user's content is empty""",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = UserProxyAgent(
    "user_proxy",
    is_termination_msg=lambda x: x.get("content", "")
    and "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",  # Don't take input from User
    code_execution_config={"use_docker": False},
)

# Initialise the Composio Tool Set
composio_tools = ComposioToolset()

# Register the preferred Applications, with right executor.
composio_tools.register_tools(
    tools=[App.LINEAR, App.GITHUB], caller=super_agent, executor=user_proxy
)

task = """For all the todos in my last commit of SamparkAI/Docs,
create a linear issue on project name hermes board and assign to right person"""

response = user_proxy.initiate_chat(super_agent, message=task)

print(response.chat_history)
