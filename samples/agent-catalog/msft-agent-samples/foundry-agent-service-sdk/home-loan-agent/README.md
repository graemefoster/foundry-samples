# 🏠 Home Loan Guide

This code sample enables agent creation to provide users with helpful information about mortgage applications at a fictitious company, Cortoso Bank.
It helps streamlines a customer's mortgage application journey, empowering them to make informed decisions about their home loan options while simplifying the documentation and application process.


## 💼 Use Cases

- **Corporate Lending Support**: Assist financial institutions in automating and scaling mortgage consultations.
- **Consumer Loan Advisory**: Help individuals evaluate loan options, understand documentation requirements, and compare payment terms.
- **Pre-Approval & Application Readiness**: Guide users through the loan readiness process with tailored documentation and eligibility support.


## 🧩 Tools

This agent leverages **Azure AI Agent Service**, using the following tools:

- **File Search** to retrieve mortgage forms, FAQs, and templates.
- **Code Interpreter** to calculate mortgage payments, compare scenarios, and validate input.

The agent is configured via a `template.py` file and deployable with Bicep for enterprise use.

## Architecture Overview

![Architecture Diagram](assets/architecture.png)

---


## ⚙️ Setup Instructions

### Prerequisites
WIP

---
## 💬 Example Agent Interactions

**User**: Can you calculate my monthly payment if I take a 30-year fixed mortgage on a $450,000 home with a $90,000 down payment at a 6.5% interest rate?  
**🔧 Agent Response**: Code Interpreter performs mortgage payment calculation.

---

**User**: What documents do I need for a Contoso Bank loan?  
**🔍 Agent Response**: File Search Tool retrieves the Contoso Bank loan documentation checklist.

---

**User**: Can you compare the estimated closing costs for FHA and Conventional loans at Contoso Bank?  
**🔍 Agent Response**: File Search Tool retrieves rows from the dataset for side-by-side cost comparison.

---

**User**: I’m comparing a 15-year and 30-year mortgage—can you show the difference in total interest paid?  
**🔧 Agent Response**: Code Interpreter compares amortization scenarios.

---

**User**: I have a condo in Florida—what loan products allow condos, and what are their DTI limits?  
**🔍 Agent Response**: File Search Tool returns products where `Allowed Property Types = Condo`, with associated DTI caps.


 
## 🛠 Customization Tips

- **Integrate with Loan Origination Systems (LOS)**  
  Add a custom tool or connector (e.g., via Azure Logic Apps) to allow users to submit pre-approval applications, upload documents, or retrieve loan status from internal LOS platforms.

- **Personalize Based on User Profile**  
  Modify the `system_message` to adjust tone and guidance for first-time buyers, military veterans, or investment property seekers.

- **Enable Secure Document Submission**  
  Extend the agent to support Azure Blob or SharePoint uploads for income verification, ID, or bank statements, and validate them using metadata or form templates.

- **Visualize Loan Comparisons**  
  Generate charts comparing monthly payments, total interest, and amortization curves across loan products.

- **Add Multi-language Support**  
  Integrate Translator or prompt-based language switching to support users in multiple languages.
