
import os
import asyncio
import streamlit as st
import sys
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# LangChain OpenAI Imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

# MCP Client Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Compatibility for ExceptionGroup (Python < 3.11)
if sys.version_info < (3, 11):
    try:
        from exceptiongroup import ExceptionGroup
    except ImportError:
        ExceptionGroup = Exception
else:
    ExceptionGroup = ExceptionGroup

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def unwrap_exception(e):
    """Recursively find the real error inside a TaskGroup/ExceptionGroup."""
    if hasattr(e, 'exceptions'):
        return ", ".join([unwrap_exception(sub) for sub in e.exceptions])
    return str(e)

async def run_agent(user_input: str):
    # Absolute path to the MCP script
    script_path = os.path.abspath("catalyst-center-mcp.py")
    
    if not os.path.exists(script_path):
        return f"File Not Found: {script_path}. Please ensure catalyst-center-mcp.py is in the same folder."

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[script_path],
        env=os.environ.copy()
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize MCP Session
                await asyncio.wait_for(session.initialize(), timeout=30.0)
                
                # Fetch tools from the MCP server
                mcp_tools_response = await session.list_tools()
                
                # Helper to convert MCP tool to LangChain StructuredTool
                def make_langchain_tool(mcp_tool):
                    async def tool_wrapper(**kwargs) -> str:
                        result = await session.call_tool(mcp_tool.name, arguments=kwargs)
                        if result.isError:
                            return f"Error from tool {mcp_tool.name}: {result.content[0].text}"
                        return result.content[0].text
                    
                    return StructuredTool.from_function(
                        coroutine=tool_wrapper,
                        name=mcp_tool.name,
                        description=mcp_tool.description
                    )

                # Create tools list
                langchain_tools = [make_langchain_tool(t) for t in mcp_tools_response.tools]
                tool_node = ToolNode(langchain_tools)
                
                # Setup LLM with OpenAI
                # Using gpt-4o for superior tool calling and larger context window
                llm = ChatOpenAI(
                    model="gpt-4o",
                    openai_api_key=os.getenv("OPENAI_API_KEY"),
                    temperature=0
                ).bind_tools(langchain_tools)

                # Define Graph Logic
                def call_model(state: State):
                    response = llm.invoke(state["messages"])
                    return {"messages": [response]}

                # Build the LangGraph
                workflow = StateGraph(State)
                workflow.add_node("agent", call_model)
                workflow.add_node("tools", tool_node)
                workflow.set_entry_point("agent")
                workflow.add_conditional_edges("agent", tools_condition)
                workflow.add_edge("tools", "agent")
                
                graph = workflow.compile()
                
                # Execute the Graph
                inputs = {"messages": [HumanMessage(content=user_input)]}
                final_state = await graph.ainvoke(inputs)
                
                return final_state["messages"][-1].content

    except Exception as e:
        return f"REAL ERROR: {unwrap_exception(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="Cisco Catalyst AI (OpenAI)", layout="wide")
st.title("🌐 Cisco Catalyst Center Assistant")
st.markdown("Query your network using OpenAI GPT-4o and MCP.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your network inventory or clients..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("OpenAI is analyzing your network..."):
            response = asyncio.run(run_agent(prompt))
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})