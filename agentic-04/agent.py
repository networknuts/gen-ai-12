from langchain_openai import ChatOpenAI 
from langgraph.graph import StateGraph, START, END 
from dotenv import load_dotenv 
from typing import TypedDict, Optional
from neo4j import GraphDatabase
import json 
import os 

# SETUP THE ENVIRONMENT
load_dotenv()
llm = ChatOpenAI(model="gpt-5.6-luna")

# NEO4J CONNECTION
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_AUTH = (NEO4J_USERNAME,NEO4J_PASSWORD)

NEO4J_DRIVER = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

# LANGGRAPH STATE
class ChatState(TypedDict):
    user_id: str 
    user_query: str 
    ai_reply: str 
    store_memory: Optional[bool]
    extracted_facts: Optional[list]

# NODE 1: CHAT NODE
def chat_node(state: ChatState):
    response = llm.invoke(state["user_query"])
    state["ai_reply"] = response.content.strip()
    print(f"AI REPLY: {state['ai_reply']}")
    return state 

# NODE 2: MEMORY CLASSIFIER NODE
def memory_classifier(state: ChatState):
    prompt = f"""
    You are a user profile memory classifier.
    Determine whether this message contains any 
    long-term personal information about the user.

    Examples of long term personal information:
    - location
    - work
    - interests
    - likes
    - dislikes

    Return the output in the following format:
    {{
        "store_memory": boolean value of true or false,
        "extracted_facts": [list of extracted facts containing long term personal information]
    }}

    User Message:
    {state['user_query']}
    """
    response = llm.invoke(prompt)
    decision = json.loads(response.content)
    state["store_memory"] = decision["store_memory"]
    state["extracted_facts"] = decision["extracted_facts"]
    return state 

# NODE 3: SAVE DATA TO NEO4J
def neo4j_save(state: ChatState):
    if not state["extracted_facts"]:
        return state 
    else:
        with NEO4J_DRIVER.session() as session:
            for fact in state["extracted_facts"]:
                session.run(
                    """
                    MERGE (u: User {id: $user_id})
                    MERGE (m: Memory {text: $fact})
                    MERGE (u)-[:HAS_MEMORY]->(m)
                    """,
                    user_id = state["user_id"],
                    fact=fact
                )
            print("SAVED MEMORY")
            return state 

# NODE 4: ROUTER NODE
def router(state: ChatState):
    if state["store_memory"]:
        return "neo4j_save"
    else:
        return END 

# BUILD AND COMPILE THE GRAPH
graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_node("memory_classifier",memory_classifier)
graph.add_node("neo4j_save",neo4j_save)

graph.set_entry_point("chat_node")
graph.add_edge("chat_node","memory_classifier")
graph.add_conditional_edges(
    "memory_classifier",
    router,
    {
        "neo4j_save": "neo4j_save",
        END: END
    }
)

app = graph.compile()

# EXECUTE THE GRAPH

def run_graph():
    user_id = input("Enter email ID: ")
    user_query = input("Human Question: ")
    app.invoke({
        "user_id": user_id,
        "user_query": user_query
    })

run_graph()