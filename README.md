
🌐 Cisco Catalyst Center AI Assistant

Python= 3.10+
OpenAI= GPT-4o
Framework= LangGraph
Interface= Streamlit

Unlock the power of conversational networking with the Cisco Catalyst Center AI Assistant. This application bridges the gap between complex network telemetry and natural language using OpenAI's GPT-4o and the Model Context Protocol (MCP).

<img width="887" height="806" alt="image" src="https://github.com/user-attachments/assets/c7826397-421e-4ec8-b981-0edb80646377" />

🚀 Key Features

🧠 Intelligent Reasoning: Powered by LangGraph, the assistant doesn't just search—it reasons through network issues, decides which tools to call, and summarizes findings.
🛠️ Dynamic Tool Discovery: Automatically imports and wraps tools from your catalyst-center-mcp.py server.
📊 Real-Time Insights: Query live inventory, client health, and network status directly from your Catalyst Center instance.
💬 Modern Chat Interface: A sleek, responsive UI built with Streamlit for a seamless user experience.
⚡ Async Performance: Built on asyncio to handle high-latency network calls without freezing the UI.


🛠️ Tech Stack

Component	Technology
LLM	OpenAI GPT-4o
Orchestration	LangChain & LangGraph
Protocol	Model Context Protocol (MCP)
Frontend	Streamlit
Language	Python 3.10+
MCP Server https://github.com/richbibby/catalyst-center-mcp (🌐Special thanks to Richbibby for his work on code)


📦 Installation & Setup

1. Clone the Repository

git clone https://github.com/HardikRaval2020/catalyst-center-mcp.git
cd cisco-catalyst-mcp

2. Install Dependencies

pip install streamlit langchain-openai langgraph mcp python-dotenv


3. Configure Your Environment 🔑

Create a .env file in the root directory:

OPENAI_API_KEY=sk-your-openai-key-here
CCC_HOST=https://1.1.1.1
CCC_USER=admin
CCC_PWD=admin


🚦 Quick Start

Ensure your MCP server script (catalyst-center-mcp.py) is in the same directory as the app. Then, launch the assistant:

streamlit run cc_mcpfrontend_openai_app_v1-4.py


🏗️ How It Works

Initialization: The app starts a background process for the MCP Server.
Tool Mapping: It inspects the MCP server to find available network functions (e.g., get_devices, get_issues).
The Brain (GPT-4o): When you ask a question, GPT-4o determines which network tool is needed.

The Loop:
Agent Node: Decides the next step.
Tools Node: Executes the Cisco API call via MCP.
Result: The agent summarizes the raw data into a human-friendly response.


🔒 Security & Best Practices

API Safety: Never hardcode your OPENAI_API_KEY. Always use the .env file.
Read-Only Access: It is recommended to use a Catalyst Center API user with read-only permissions for general querying.
Error Handling: The app includes a recursive exception unwrapper to help debug complex MCP connection issues.


Developed for the next generation of Intent-Based Networking. 🌐💡
