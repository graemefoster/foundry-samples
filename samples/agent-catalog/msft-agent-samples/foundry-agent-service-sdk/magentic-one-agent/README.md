# 🧠 MagenticOne Agent

This code sample showcases a generalist, autonomous multi-agent system that performs deep research and problem-solving by orchestrating web search, code generation, and code execution agents. Helpful for tackling open-ended analytical or technical tasks.

---

## 💼 Use Cases

- **Multi-Source Reasoning**: Pull together content from search engines, websites, and structured files to form a grounded response.
- **Technical Problem Solving**: Execute and validate small-scale Python code to solve algorithmic or data wrangling tasks.
- **Complex Web Queries**: Navigate unstructured questions by orchestrating real-time web search and document parsing.
- **Agent Demos or Debugging**: Use as a scaffold to test autonomous planning and coordination in agent graphs.

---

## 🧩 Tools & Capabilities

Built with **Azure AI Agent Service**, the MagenticOne agent graph includes:

- **Planner Agent (`magneticOneCode.agent`)** to break down the user’s high-level task into smaller, tractable goals.
- **WebBrowse Agent** to simulate multi-turn browsing and interaction with live websites.
- **BingSearch Agent** to retrieve recent or factual content with citation grounding.
- **CodeExecutor Agent** to perform lightweight computation, validation, or summarization of structured data.

The agent graph and routing configuration are defined declaratively in `.agent` and `.fdl` files.

---

## 🧠 Architecture Overview

![Architecture Diagram](assets/architecture-magenticone.png)

---

## ⚙️ Setup Instructions

### Prerequisites

- An Azure AI Project with Agent Service enabled
- Azure AI Agent SDK and dependencies (`requirements.txt`)
- Agent files: `magneticOneCode.agent`, `webBrowse.agent`, `codeExecutor.agent`, `BingSearch.agent`
- Orchestration graph: `magentic.one.fdl`

---

## 💬 Example Agent Interactions

**User**: Can you find the latest benchmarks for GPT-4 on reasoning tasks and compare them to Claude 3?  
**🌐 Agent Response**: BingSearch gathers content → WebBrowse validates source → Summarizer produces side-by-side results

---

**User**: What’s the Python code to calculate BLEU score from two text files?  
**💻 Agent Response**: Planner routes to CodeExecutor with import and scoring logic

---

**User**: Read the OpenAI DevDay transcript and summarize new agent features by category.  
**📖 Agent Response**: WebBrowse extracts the transcript → CodeExecutor categorizes → Final structured output delivered

---

**User**: Which generative AI tools support document-level RAG and schema control?  
**🔎 Agent Response**: Planner routes task to BingSearch → WebBrowse extracts pros/cons → Summary grounded in retrieved URLs

---

## 🛠 Customization Tips

- **Replace BingSearch with FileSearch**: To handle documents uploaded to your Azure AI Project.
- **Extend Code Execution**: Add guards or more libraries to run evals, format charts, or parse JSON.
- **Test Autonomous Mode**: Run planner + tools with minimal user prompting for an agent demo.
- **Adapt for Voice Agents**: Combine with Voice Live Agent to make this a spoken assistant for devs or analysts.

---

## 📁 Files Included

- `magneticOneCode.agent` — primary planner agent
- `webBrowse.agent` — browser simulation for agent exploration
- `BingSearch.agent` — fetches grounded real-time results
- `codeExecutor.agent` — evaluates and returns Python logic or math
- `
