# 💬 Customer Support Agent

This is a code sample for a multi-phase workflow built with Azure AI Agent Service, designed to assist customers with secure authentication and billing inquiries. It uses a state-based orchestration to verify customer identity and retrieve billing information, while supporting human-in-the-loop escalation.

---

## 💼 Use Cases

- **Customer Authentication**: Verify users through ID or account number prior to handling sensitive queries.
- **Billing Inquiry Support**: Retrieve and explain billing details for a verified account.
- **Agent Escalation Readiness**: Stream output to users and fallback to human-in-loop if input or context is missing.
- **Workflow Handoff**: Easily expandable to handle follow-ups like payment assistance, usage summaries, or complaint handling.

---

## 🧩 Tools & Capabilities

This agent is orchestrated using **Azure AI Agent Service** with the following states and components:

### 🔐 `Authentication` State

- **Agent**: `CustomerAuthenticator`  
- **Purpose**: Validates the customer and extracts a `CustomerId`
- **Human-in-the-loop**: Enabled on missing input or failed authentication
- **Output**:  
  - `CustomerAccount → CustomerId`

---

### 💳 `Billing` State

- **Agent**: `CustomerServiceAgent`  
- **Purpose**: Retrieves customer billing details using `CustomerId` as input
- **Human-in-the-loop**: Enabled if no message or context is missing
- **Input**:  
  - `accountNumber ← CustomerId`

---

### 🧭 Workflow Overview

| State            | Description                            | Agent                | Transition Event       |
|------------------|----------------------------------------|----------------------|------------------------|
| Authentication   | Validates customer identity            | `CustomerAuthenticator` | `CustomerValidated`    |
| Billing          | Provides billing information           | `CustomerServiceAgent`   | `ConversationEnd`      |
| End              | Terminates conversation                | *None*               | —                      |

---

## ⚙️ Setup Instructions

### Prerequisites

1. Azure subscription with the following permissions
   - Contributor or Cognitive Services Contributor role (for resource deployment)
   - Azure AI Developer and Cognitive Services user role (for agent creation)
2. Agent setup: deploy the latest agent setup using this ([custom deployment](https://www.aka.ms/basic-agent-deployment)).
   - The above creates:
      - AI Services resource
      - AI Project
      - Model deployment
3. Python 3.8+
4. Azure CLI
   
- Agent files:
  - `CustomerAuthenticator.agent`
  - `CustomerServiceAgent.agent`
- Declarative file (e.g., `customer_support_workflow.fdl` or JSON shown above)
- Supporting documents or mock data (optional):  
  - Customer profiles  
  - Sample
