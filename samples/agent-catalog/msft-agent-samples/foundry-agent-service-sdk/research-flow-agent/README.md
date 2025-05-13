# 🧠 ResearchFlow Agent

This agent orchestrates a multi-step research AI workflow, helping users gather, synthesize, and structure knowledge from complex sources. Ideal for analysts, strategists, product teams, and technical writers.

---

## 💼 Use Cases

- **Market & Competitive Research**: Automate the collection and summarization of competitor data, trends, and product insights.
- **Technical Literature Review**: Extract structured summaries from technical documents and API documentation.
- **Customer Deep Dives**: Combine customer feedback, CRM notes, and meeting transcripts into coherent insight packs.
- **Strategic Briefing Packs**: Generate polished summaries, outlines, and visual insights for leadership-ready deliverables.

---

## 🧩 Tools & Capabilities

This agent is built with **Azure AI Agent Service** and typically integrates:

- **File Search** to extract and cross-reference details from uploaded PDFs, Markdown, and structured datasets.
- **Summarizer Agent** to generate section-level summaries from technical or dense input.
- **Planner Agent** to break large prompts into logical subtasks and route them to specialized sub-agents.
- **Progress Tracker or Router Agent** to manage task completion and coordination across a multi-agent graph.

The agent orchestration is defined using `.agent` and `.fdl` configuration files.

---

## 🧠 Architecture Overview

![Architecture Diagram](assets/architecture-researchflow.png)

---

## ⚙️ Setup Instructions

### Prerequisites

- An Azure AI Project with Agent Service enabled
- Azure AI Agent SDK and required packages (see `requirements.txt`)
- Project files for: `ResearchFlow.agent`, `Summarizer.agent`, `LedgerPlanner.agent`, etc.

---

## 💬 Example Agent Interactions

**User**: Can you generate a competitive landscape analysis on cloud-native agent orchestration tools?  
**📥 Agent Response**: Planner routes task to summarizer + file search, returning a 3-part overview (market size, players, differentiators)

---

**User**: I uploaded three analyst reports—can you extract the trends relevant to SMB adoption and turn it into a leadership summary?  
**📄 Agent Response**: File Search → Summarizer → Final summary document with key stats, quotes, and predictions.

---

**User**: What's the breakdown of feature gaps between our platform and Company X?  
**📊 Agent Response**: File Search identifies platform docs; Summarizer creates comparative feature tables.

---

**User**: I'm prepping a 2-minute pitch—summarize these 10 pages of product reviews into themes I can speak to.  
**🧠 Agent Response**: Sentiment clustering and summarization into 3 key talking points with example quotes.

---

## 🛠 Customization Tips

- **Add Custom Tools**: Plug in web search or vector DB search to complement file-based knowledge.
- **Tune Agent Routing**: Adjust the planner or agentRouter logic to improve task delegation.
- **Control Summarization Style**: Modify the summarizer agent’s system prompt for narrative, factual, or bullet-style summaries.
- **Export as Report or Slide Deck**: Add downstream tools that turn outputs into formatted PDFs or PowerPoint slides.

---

## 📁 Files Included

- `ResearchFlow.agent` — main orchestration agent
- `Summarizer.agent` — task-specific summarizer
- `LedgerPlanner.agent` — planner for prompt decomposition
- `progressManager.agent` — optional tool for managing intermediate steps
- `DeepResearchAgent.fdl` — agent graph and tool configuration

---


