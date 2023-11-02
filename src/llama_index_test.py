# Import and initialize our tool spec
# Setup OpenAI Agent
import openai
from config.config import cfg
openai.api_key = cfg.openai_api_key
from llama_index.agent import OpenAIAgent
from llama_hub.tools.database.base import DatabaseToolSpec


db_spec = DatabaseToolSpec(
    scheme = "postgresql", # Database Scheme
    host = cfg.pg_host, # Database Host
    port = cfg.pg_port, # Database Port
    user = cfg.pg_user, # Database User
    password = cfg.pg_password, # Database Password
    dbname = cfg.pg_database # Database Name
)

tools = db_spec.to_tool_list()
for tool in tools:
    print(tool.metadata.name)
    print(tool.metadata.description)
    print(tool.metadata.fn_schema)

agent = OpenAIAgent.from_tools(tools, verbose=True)

while True:
    print(agent.chat(input("Enter a question: ")))