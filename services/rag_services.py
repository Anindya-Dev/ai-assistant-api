from agents.agent import run_agent
from agents.tools import search_documents, answer_directly
from agents.prompts import build_rag_prompt, build_rewrite_prompt
from services.llm_service import generate_response

def handle_query(query:str,user_id: int):
    agent_response=run_agent(query)

    if agent_response["tool"]== "search_documents":
        current_query=query
        for attempt in range(4):
            result= search_documents(current_query,user_id)
            documents=result["documents"]
            distances=result["distances"]


            if documents and distances and distances[0]<=1:
                context="\n".join(documents)
                prompt=build_rag_prompt(context,current_query)
                return generate_response(prompt)
            rewrite_prompt=build_rewrite_prompt(current_query)
            current_query=generate_response(rewrite_prompt).strip().strip('"') #.strip().strip('"') removes extra whitespace and quotes if the model still adds them
            
        return "I couldn't find anything relevant in your journal entries."


    else:
        result=answer_directly(agent_response["query"])
    
    return result
