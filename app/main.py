from fastapi import FastAPI
from pydantic import BaseModel
import os
import json

# ----------------------------
# Simple Tool Definitions
# ----------------------------

def calculator_tool(expression: str) -> str:
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


TOOLS = {
    "calculator": calculator_tool
}

# ----------------------------
# Agent Logic (Mock LLM Reasoning)
# ----------------------------

def agent_reasoning(user_input: str):
    """
    Very simple agent logic:
    - If math detected → use calculator tool
    - Else → respond directly
    """
    if any(char.isdigit() for char in user_input):
        return {
            "tool": "calculator",
            "input": user_input
        }
    else:
        return {
            "response": f"Agent response: {user_input}"
        }

# ----------------------------
# FastAPI App
# ----------------------------

app = FastAPI(title="LLM Agent Tool Server")

class AgentRequest(BaseModel):
    message: str

class AgentResponse(BaseModel):
    result: str
    used_tool: str | None = None

@app.post("/agent/run", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    decision = agent_reasoning(request.message)

    if "tool" in decision:
        tool_name = decision["tool"]
        tool_input = decision["input"]
        tool_fn = TOOLS.get(tool_name)

        if tool_fn:
            output = tool_fn(tool_input)
            return AgentResponse(result=output, used_tool=tool_name)

        return AgentResponse(result="Tool not found", used_tool=tool_name)

    return AgentResponse(result=decision["response"])
