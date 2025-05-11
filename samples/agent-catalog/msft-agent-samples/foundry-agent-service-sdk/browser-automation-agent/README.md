# 🌐 Browser Automation Agent

This agent enables AI-powered browser automation using Azure AI Agent Service and the Azure Playwright tool. It is designed to perform web-based tasks such as searching, scraping, summarizing, and interacting with dynamic websites in a secure and automated way.

**WARNING:** Browser automation comes with significant security risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages which the AI encounters may cause it to execute commands you do not intend, which could compromise the security of your browser, your computer, and any accounts to which the browser or AI has access, including personal information, financial, or enterprise systems. We recommend that you use this type of agent only in isolated environments with controlled access, such as browsers running within dedicated VMs.

---

## 💼 Use Cases

- **Web Research & Data Collection**: Extract structured data from public web pages, forms, or dynamic tables.
- **Competitive Monitoring**: Retrieve pricing, reviews, or feature information from competitor websites.
- **Recipe, Travel, or Product Discovery**: Perform contextual searches and generate organized summaries.
- **Customer Support Tasks**: Automatically navigate portals to retrieve account status, ticket updates, etc.

---

## 🧩 Tools

This agent leverages **Azure AI Agent Service** and uses:

- **Browser Automation Tool** (via Playwright): Executes browser-based tasks on your behalf, securely and asynchronously.

The agent is configured through a Python script (`browser_automation.py`) and authenticated using Azure identity.

---

## 🧠 Architecture Overview

![Architecture Diagram](assets/architecture-browser-automation.png)

---

## ⚙️ Setup Instructions

### Prerequisites

- Azure AI Foundry project
- A deployed language model (e.g., GPT-4)
- Playwright connection (optional, see below)

### Environment Variables

Set the following environment variables before running the sample:

```bash
PROJECT_CONNECTION_STRING=<your_project_connection_string>
MODEL_DEPLOYMENT_NAME=<your_model_deployment_name>
PLAYWRIGHT_CONNECTION_ID=<optional_serverless_connection_id>
