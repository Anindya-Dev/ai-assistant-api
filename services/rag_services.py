from agents.agent import run_agent
from agents.tools import search_documents, answer_directly

def handle_query(query:str):
    agent_response=run_agent(query)

    if agent_response["tool"]== "search_documents":
        result=search_documents(agent_response["query"])
    else:
        result=answer_directly(agent_response["query"])
    
    return result