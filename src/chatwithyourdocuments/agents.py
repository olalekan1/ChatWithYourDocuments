import os
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain_core.vectorstores import VectorStore
from chatwithyourdocuments.prompts import RAG_WORKFLOW_INSTRUCTIONS, CHUNK_ANALYST_INSTRUCTIONS, SUBAGENT_DELEGATION_INSTRUCTIONS
from dotenv import load_dotenv
from chatwithyourdocuments.tools import backend, create_search_documents_tool

load_dotenv()

def build_agent(
    vector_store: VectorStore,
    max_concurrent_analysts: int = 3,
):
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

    search_documents = create_search_documents_tool(vector_store)

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

    return agent

