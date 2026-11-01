import os
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from chatbotwithlangchain.prompts import RAG_WORKFLOW_INSTRUCTIONS, CHUNK_ANALYST_INSTRUCTIONS, SUBAGENT_DELEGATION_INSTRUCTIONS
from dotenv import load_dotenv
from chatbotwithlangchain.tools import search_documents, backend

load_dotenv()

max_concurrent_analysts = 3

INSTRUCTIONS = (
    RAG_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "="*80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(max_concurrent_analysts=max_concurrent_analysts)
)

chunk_analyst_subagent = {
    "name": "chunk-analyst",
    "description": (
        "Analyzes one retrieved document chunk file. "
        "Pass the user's question and one file path under /retrieved/."
    ),
    "system_prompt": CHUNK_ANALYST_INSTRUCTIONS,
}

query = "Summarise my CV and cover letter and list my most important skills and experience. Include inline links to the source documents."

model = init_chat_model(
    model="openai/gpt-5-nano",
    model_provider="openai",
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)


agent = create_deep_agent(
    model=model,
    tools=[search_documents],
    backend=backend,
    system_prompt=INSTRUCTIONS,
    subagents=[chunk_analyst_subagent]
)

result = agent.invoke(
    {
        "messages": [HumanMessage(content=query)]
    }
)

print("Final Answer:\n")
print(result["messages"][-1].content)