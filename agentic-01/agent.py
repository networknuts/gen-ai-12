from langchain_openai import ChatOpenAI 
from langgraph.graph import StateGraph, START, END 
from dotenv import load_dotenv 
from typing import TypedDict 

# SETUP THE AI ENVIRONMENT
load_dotenv()
llm = ChatOpenAI(model="gpt-5.6-luna")

# STEP 1: DEFINE THE STATE
class CodingState(TypedDict):
    user_request: str 
    code: str 
    rating: int 

# STEP 2: CREATING THE NODES

# NODE 1: DEVELOPER NODE
def develop_code(state: CodingState):
    response = llm.invoke(
        f"""
        Write code for the following user requirement:
        {state['user_request']}

        Return the code in plain text format.
        """
    )
    return {
        "code": response.content 
    }

# NODE 2: QA NODE
def judge_code(state: CodingState):
    response = llm.invoke(
        f"""
        Review the given code on the following parameters:
        - Error handling
        - Modern code practices
        - Scalability

        Provide a single rating between 1-10 after judging the code on the above parameters.

        Code:
        {state['code']}

        Important: Only return the rating in an integer format between 1-10
        """
    )
    return {
        "rating": response.content 
    }

# STEP 3: BUILDING THE RELATIONSHIP BETWEEN NODES

graph = StateGraph(CodingState)

graph.add_node("developer",develop_code)
graph.add_node("qa",judge_code)

graph.add_edge(START,"developer")
graph.add_edge("developer","qa")
graph.add_edge("qa",END)

# COMPILE THE GRAPH
app = graph.compile()

# STEP 4: RUNNING THE AGENT
user_request = input("Enter idea to create code for: ")

result = app.invoke({
    "user_request": user_request,
    "code": "",
    "rating": ""
})

print("\nAI AGENT OUTPUT\n")
print("GENERATED CODE")
print(result['code'])

print("RATING")
print(result['rating'])