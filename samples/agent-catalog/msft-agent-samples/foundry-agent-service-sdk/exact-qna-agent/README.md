# Exact Question Answering Agent

## Summary
The **Exact Question Answering Agent** is an AI-powered agent built using Azure AI Agent Service, together with Custom Question Answering in Azure AI Language. It provides exact answering, perfect for deterministic question answering with human controls. With it, businesses can have top questions that covers say 90% of their business applications handled by human exact answering, then have LLM RAG solution handle long tails, while routing complex queries to human agents.

## Use Cases
1. **Customer Support**: Automate deterministic humnan-controlled responses to frequently asked or high value questions such as “What is your return policy?”, “How do I reset my password?”, or “What’s the warranty coverage?” while routing complex queries to human agents.
2. **IT Support**: Provide percise answers like “What is the VPN setup process?”, “Where do I download the latest security patch?”, or “How do I enroll in 2FA?” faithful to technical documentation and internal IT knowledge bases.
3. **Education and Student Help**: Respond with percise and human-controlled answers to questions like “What’s the deadline to drop a course?”, “Where do I submit my financial aid application?”, or “What’s the grading policy for AP credits?” faithful to school and academic documentation.

## Architecture Overview
The system consists of:
- An AI Agent created with Azure AI Agent Service using `gpt-4o` as the base model.
- Custom Question Answering for precise responses.
- A Bicep template to automate provisioning of Azure resources.

```text
+----------------+                         
|   User Query   |                         
| (Any Intent)   |                         
+-------+--------+                         
        |                                  
        v                                  
+-----------------+                invokes                        
|                 |-------------------------------------->   +------+
| Exact Question  |<--------------------------------------   | CQA  |
| Answering Agent |             exact answering              +------+
+-----------------+   
        |               
        v                                  
+-------------------------------------+           
| Agent Response with exact answer    |           
|                                     |           
+-------------------------------------+           

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
| `project_endpoint`                     | Endpoint for the project this agent is using                      |
| `model_name`                           | name of the model to be used for the Agent                        |
| `connection_id`                        | Connection ID for the language resource in the AI Foundry         |
| `amlWorkspaceResourceName`             | Name of the AI Project or the AML workspace                       |

## Sample Data Instructions
This repo contains a `sample_data/` directory with:
- Product knowledge base of a fictional outdoor retail company, Contoso Outdoor.

You can test the interaction by invoking the agent with prompts like:
## Example Agent Interaction
### User: 
what is your return policy

### Agent: 
We offer a 30-day return policy on most items. If you are not satisfied with your purchase, you can return it for a full refund or exchange it for another product, as long as:

The item is unused, unworn, and in its original packaging.
You provide proof of purchase (order confirmation or receipt).
The return request is made within 30 days of receiving the item.

Certain items, such as personalized, clearance, or final sale products, may not be eligible for return. To start a return or exchange, visit our Returns & Exchanges page and follow the step-by-step instructions. We may provide a prepaid return label, but shipping fees for returns may apply.

### User: 
What tents are recommended for winter?

### Agent: 
For winter camping, neither the Alpine Explorer Tent nor the TrailMaster X4 Tent is specifically recommended for extreme winter conditions. Here are the details:

Alpine Explorer Tent:
Designed primarily for 3-season use. It can withstand light snowfall but may not support heavy snow or extreme winter conditions.
TrailMaster X4 Tent:
Also designed for 3-season use, not suitable for extreme winter conditions with heavy snow and freezing temperatures.
In summary, both tents are considered 3-season tents and may not provide adequate support for severe winter weather.

### User: 
What mountain boots are good for a casual climber?

### Agent: 
For casual climbers, I recommend the following boots:

TrekReady Hiking Boots
Comfort: Incredibly comfortable and durable.
Traction: Excellent traction and waterproof design, ideal for various hiking adventures.
Support: Features a high-top design and padded collar for great ankle support.
Break-in Period: May require some time to break in for maximum comfort.
Versatile Use: Designed primarily for hiking but can also be worn for everyday activities.
TrailWalker Hiking Shoes
Lightweight: Good for long hikes due to their lightweight design.
Waterproof: Keeps feet dry during unexpected rain.
Support: Provides excellent ankle support and comfort, although some users report slight discomfort around the toe area after extended use.
Good Traction: Features outstanding grip, suitable for challenging trails.
Both options offer excellent features for casual climbing and hiking.

## Customization Tips
- Modify the system instructions in `agent.py` to your needs or preferences (e.g., style of answering).
- Extend the agent with other useful tools or APIs (using OpenAPI spec).
- Fine-tuning the associated CQA deployment, e.g. adding/modify/delete question-answer paires, or finetune questions, etc.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.