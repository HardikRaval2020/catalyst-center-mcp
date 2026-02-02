
Cisco Catalyst Center AI Assistant (MCP + LangGraph)

This project provides a natural language interface for Cisco Catalyst Center (formerly DNA Center). By leveraging the Model Context Protocol (MCP), LangGraph, and Groq, users can query network inventory, site hierarchies, and client analytics using plain English.

Special Thanks to Richbibby for MCP Server code available at : https://github.com/richbibby/catalyst-center-mcp

🚀 Features

Natural Language Network Queries: Ask questions like "How many unreachable devices do I have?" or "Show me wireless clients connected in the last 2 hours."
MCP Server Integration: A custom FastMCP server that bridges the Catalyst Center REST APIs to an LLM.
Intelligent Reasoning: Uses LangGraph to handle multi-step tasks (e.g., converting "last 2 hours" into epoch timestamps before querying client data).
Interactive UI: A clean, responsive chat interface built with Streamlit.
Token-Optimized: Data is compacted before being sent to the LLM to stay within Groq's rate limits.

🛠️ Tech Stack

LLM: Groq (Llama 3 70B)
Orchestration: LangChain & LangGraph
Protocol: Model Context Protocol (MCP) via fastmcp
Frontend: Streamlit
Network API: Cisco Catalyst Center REST API

📋 Prerequisites

Python 3.10 or higher
Access to a Cisco Catalyst Center instance
A Groq API Key

🔧 Installation & Setup

Clone the Repository

bash
Copy Code
git clone https://github.com/your-username/catalyst-center-ai.git
cd catalyst-center-ai
Create a Virtual Environment

bash
Copy Code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy Code
pip install fastmcp requests python-dotenv langchain langchain-groq langgraph streamlit mcp urllib3 pydantic
Configure Environment Variables Create a .env file in the root directory:

env
Copy Code
CCC_HOST=https://your-catalyst-center-ip
CCC_USER=your-username
CCC_PWD=your-password
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=available_groq_model

🖥️ Usage

Start the Application Run the Streamlit frontend, which will automatically initialize the MCP server in the background:

bash
Copy Code
streamlit run app.py
Example Queries

"List the first 5 devices in my network."
"What is the site hierarchy for my organization?"
"How many wireless clients were active today?"
"Show me the interfaces for device [Device_ID]."

🏗️ Project Structure

app.py: The main entry point. Contains the Streamlit UI and the LangGraph agent logic.
catalyst-center-mcp.py: The MCP server defining the tools (API wrappers) available to the AI.
.env: (Ignored by git) Stores sensitive credentials.

⚠️ Troubleshooting

413 Request Too Large: This happens if the API returns too much data. The fetch_devices tool is optimized to return only essential fields.
TaskGroup Error: Usually caused by print() statements in the MCP server script. Ensure all logs in catalyst-center-mcp.py are redirected to sys.stderr.
SSL Warnings: The script bypasses SSL verification for lab environments. Ensure your CCC_HOST includes https://.
