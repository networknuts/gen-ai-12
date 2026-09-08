from langchain_openai import ChatOpenAI 
from langgraph.graph import StateGraph, START, END 
from dotenv import load_dotenv 
from typing import TypedDict 
import json 

# SETUP THE AI ENVIRONMENT
load_dotenv()
llm_developer = ChatOpenAI(model="gpt-5.6-luna")
llm_qa = ChatOpenAI(model="gpt-5.6-sol")

MAX_RETRIES = 3

# STEP 1: DEFINE THE STATE
class CodingState(TypedDict):
    user_request: str 
    code: str 
    rating: int
    retries: int 
    feedback: str 
    status: str 

# STEP 2: CREATING THE NODES

# NODE 1: DEVELOPER NODE
def develop_code(state: CodingState):
    prompt = f"""
        Write Java code for the following user requirement:
        {state['user_request']}

        If feedback is provided, improve the previous version of the code.
        Previous Code:
        {state['code']}

        Feedback:
        {state['feedback']}

        Only return the code, no markdown.
        """
    result = llm_developer.invoke(prompt).content.strip()
    return {
        "code": result,
        "feedback": ""
    }


# NODE 2: QA NODE
def qa_node(state: CodingState):
    prompt = f"""
    You are a senior QA Java Engineer.
    Evaluate the code for the given parameters:
    - Correctness of the code
    - Structure of the code
    - Readability of the code
    - Is the code following best industry practices
    - Error handling of the code
    - Scalability of the code
    - Vulnerabities in the code

    Return the output in the following dict format:
    {{
        "rating": integer value between 1-10,
        "feedback": string value with clear explanations of improvements to make to the code
    }}

    Code:
    {state['code']}
    """
    ai_output = llm_qa.invoke(prompt).content.strip()
    result = json.loads(ai_output)
    return {
        "rating": int(result['rating']),
        "feedback": result['feedback']
    }

# NODE 3: APPROVAL NODE
def set_approved(state: CodingState):
    return {"status": "approved"}

# NODE 4: FAILURE NODE
def set_failed(state: CodingState):
    return {"status": "failed"}

# NODE 5: INCREMENTAL RETRY LOGIC NODE
def incremental_retry(state: CodingState):
    return {"retries": state['retries']+1}

# NODE 6: ROUTING NODE
def check_rating(state: CodingState):
    if state['rating'] >= 7:
        return "approved"
    if state['retries'] >= MAX_RETRIES:
        return "failed"
    return "retry"


# STEP 3: BUILDING THE RELATIONSHIP BETWEEN NODES

graph = StateGraph(CodingState)

graph.add_node("developer",develop_code)
graph.add_node("qa",qa_node)
graph.add_node("approval",set_approved)
graph.add_node("failure",set_failed)
graph.add_node("retry",incremental_retry)

graph.set_entry_point("developer")

graph.add_edge("developer","qa")
graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approval",
        "failed": "failure",
        "retry": "retry"
    }
)
graph.add_edge("approval",END)
graph.add_edge("failure",END)
graph.add_edge("retry","developer")

# COMPILE THE GRAPH
app = graph.compile()

# STEP 4: RUNNING THE AGENT
user_request = input("Enter idea to create java code for: ")

result = app.invoke({
    "user_request": user_request,
    "code": "",
    "rating": 0,
    "feedback": "",
    "retries": 0,
    "status": "running"
})

print("\nAI AGENT OUTPUT\n")
print("GENERATED CODE")
print(result['code'])

print("FEEDBACK")
print(result['feedback'])

print("RATING")
print(result['rating'])

print("RETRIES USED")
print(f"Retries: {result['retries']}")

print("STATUS")
print(f"Status: {result['status']}")