# Intent Routing Agent

## Summary
The **Intent Routing Agent** is an AI-powered agent built using Azure AI Agent Service, together with Conversational Language Understanding (CLU) and Custom Question Answering (CQA) in Azure AI Language. It detects user intent and provides exact answers, perfect for deterministic intent routing and precise question answering with human controls. With it, businesses can handle top intents and questions that cover, say, 90% of their business applications using human-controlled intent detection and question answering, while leveraging LLM RAG solutions to handle long-tail queries.

## Use Cases
1. **Customer Support**: Identify user intent (e.g., "cancel my order" vs. "where is my package") to eanble routing to deterministic workflows accordingly. Forfrequently asked or high value questions (e.g., return policy, warranty info), provide precise answers from a verified knowledge base.  
2. **E-commerce**:Detect customer shopping intents such as comparing products or tracking orders. Offer fact-based answers like “Which jackets are waterproof under $200?” or “When will my order arrive?”—while handing off complex support needs to a human.
3. **Banking and Finance**:Recognize intents like “check my balance,” “dispute a charge,” or “find mortgage options.” to enable deteministic intent fulfillment routing. Provide percise answers such as interest rates, statement breakdowns, or loan requirements, with built-in guardrails for compliance.


## Architecture Overview
The system consists of:
- An AI Agent created with Azure AI Agent Service using `gpt-4o` as the base model.
- Conversational Language Understanding for intent detection.
- Custom Question Answering for precise responses.
- A Bicep template to automate provisioning of Azure resources.

```text
+----------------+                         
|   User Query   |                         
| (Any Intent)   |                         
+-------+--------+                         
        |                                  
        V                         invokes                         
+-----------------+ --------------------------------------------------->   +------+
|                 |<----------------------------------------------------   |  CLU |
| Intent Routing  |      detected intent (predefined, or undefined)        +------+
|                 |        
|       Agent     |        invoke if quesiton intent is detected            +------+
|                 |----------------------------------------------------->   |  CQA |
+-----------------+<-----------------------------------------------------   +------+
        |                        exact answers                
        v                                  
+-------------------------------------------------+           
| Agent Response with detected intent             |           
| or exact answer if question intent is detected  |           
+-------------------------------------------------+           

```
## Setup Instructions

### Prerequisites
- Python 3.8+
- Azure CLI
- Azure subscription
- Agent setup: deploy the latest agent setup using ([this custom deployment](https://github.com/azure-ai-foundry/foundry-samples/tree/main/use-cases/agents/setup/basic-setup)).
  - The above creates:
    1. AI Services resource (type: Microsoft.CognitiveServices/accounts),
    2. AI Project (type: Microsoft.CognitiveServices/accounts/projects),
    3. Model deployment (type: Microsoft.CognitiveServices/accounts/deployments) 

### Steps
1. **Clone the Repository**

2. **Set Environment Variables**
```bash
PROJECT_ENDPOINT="<your-project-endpoint>" (https://<your-ai-services-account-name>.services.ai.azure.com/api/projects/<your-project-name>)
MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
```

3. **Deploy Resources Using Bicep**
```bash
 az deployment group create \
   --resource-group <your-rg> \
   --template-file deploy.bicep \
   --parameters \
     clu_project="<clu_project>" \
     clu_deployment= "<clu_deployment>" \
     cqa_project="<cqa_project>" \
     cqa_deployment= "<cqa_deployment>" \
     amlWorkspaceResourceName="<AI-Project-Name>"
```

4. **Run the Agent Script**
```bash
 python agent.py
```

## ⚙️ Configuration Guide
| Parameter Name                         | Description                                                       |
|----------------------------------------|-------------------------------------------------------------------|
| `language_resource_url`                | Endpoint for the language resource                                |
| `language_resource_connection_name`    | Connection name for the language resource in the AI Foundry       |
| `cqa_project_name`                     | Unique name for the CQA project this agent is using               |
| `cqa_deployment_name`                  | Unique name for the CQA deployment this agent is using            |
| `clu_project_name`                     | Unique name for the CLU project this agent is using               |
| `clu_deployment_name`                  | Unique name for the deployed CLU model under the clu_project      |
| `project_endpoint`                     | Endpoint for the project this agent is using                      |
| `model_name`                           | Name of the model to be used for the Agent                        |
| `connection_id`                        | Connection ID for the language resource in the AI Foundry         |
| `amlWorkspaceResourceName`             | Name of the AI Project or the AML workspace                       |

## Sample Data Instructions
This repo contains a `sample_data/` directory with:
- Product knowledge base of a fictional outdoor retail company, Contoso Outdoor.

You can test the interaction by invoking the agent with prompts like:
## Example Agent Interaction

### User: 
Where is my order?

### Agent:
Detected Intent: CheckOrderStatus

### User: 
i need change my shipping destination

### Agent: 
Detected Intent: UpdateShippingInfo


### User: 
I need ro return my order

### Agent: 
Detected Intent: ProcessReturnsAndExchanges

### User: 
what is your return policy

### Agent: 
We offer a 30-day return policy on most items. If you are not satisfied with your purchase, you can return it for a full refund or exchange it for another product, as long as:

The item is unused, unworn, and in its original packaging.
You provide proof of purchase (order confirmation or receipt).
The return request is made within 30 days of receiving the item.

Certain items, such as personalized, clearance, or final sale products, may not be eligible for return. To start a return or exchange, visit our Returns & Exchanges page and follow the step-by-step instructions. We may provide a prepaid return label, but shipping fees for returns may apply.

## Customization Tips
- Modify the system instructions in `agent.py` to your needs (e.g., style of responding).
- Fine-tuning the associated CLU deployment, e.g. adding/modify/delete intents or entities etc
- Fine-tuning the associated CQA deployment, e.g. adding/modify/delete question-answer paires, or finetune questions, etc
- Extend the agent with other useful tools or APIs (using OpenAPI spec).


## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.