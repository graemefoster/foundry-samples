# Travel Planner Agent

## Summary
The **Travel Planner Agent** is an AI-powered agent built using Azure AI Agent Service. It helps users receive up-to-date travel recommendations by leveraging both the **Bing Grounding Tool** and the **TripAdvisor API**. The agent summarizes relevant information clearly and offers to create a custom itinerary based on the user's travel duration.

## Use Cases
1. **Vacation Planning**: Travelers can get up-to-date suggestions on destinations, hotels, and activities.
2. **Business Travel**: Professionals receive efficient recommendations tailored to time-sensitive trips.
3. **Local Exploration**: Residents or tourists can find trending events, attractions, or day-trip ideas in their vicinity.

## Architecture Overview
The system consists of:
- An AI Agent created with Azure AI Agent Service using `gpt-4o` as the base model.
- A Bing Grounding Tool integrated via Azure Bing Account and connected to the agent.
- A TripAdvisor API tool integrated via OpenAPI.
- A Bicep template to automate provisioning of Azure resources.

```text
+----------------+                         
|   User Query   |                         
| (Travel Only)  |                         
+-------+--------+                         
        |                                  
        v                                  
+-------------------+        invokes        +----------------------------+
|  Travel Planner | ------------------->  | Bing Grounding Tool (API)  |
|     (AI Agent)    | ------------------->  | TripAdvisor API (OpenAPI)  |
+-------------------+        results        +----------------------------+
        |                                  
        v                                  
+------------------------------+           
| Agent Response with summary  |           
| and optional itinerary prompt|           
+------------------------------+           
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Azure CLI
- Azure subscription
- Agent setup: deploy the latest agent setup using ([this custom deployment](https://github.com/azure-ai-foundry/foundry-samples/tree/main/use-cases/agents/setup/basic-setup)).
  - The above creates:
    1. AI Services resource
    2. AI Project
    3. Model deployment 
- Bing Grounding resource
- TripAdvisor API connection (via OpenAPI)

### Steps
1. **Clone the Repository**

2. **Set Environment Variables**
```bash
PROJECT_ENDPOINT="<your-project-endpoint>" # (https://<your-ai-services-account-name>.services.ai.azure.com/api/projects/<your-project-name>)
MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"
BING_CONNECTION_ID="<your-bing-connection-id>"
TRIPADVISOR_CONNECTION_ID="<your-tripadvisor-connection-id>"
```

3. **Deploy Resources Using Bicep**
```bash
 az deployment group create    --resource-group <your-rg>    --template-file bing-grounding.bicep    --parameters      bingAccountName="bing-grounding-agent"      bingSku="S1"      connectionName="bing-grounding-conn"      amlWorkspaceResourceName="<AI-Project-Name>"
```

4. **Run the Agent Script**
```bash
 python agent.py
```

## ⚙️ Configuration Guide
| Parameter Name             | Description                                                       |
|----------------------------|-------------------------------------------------------------------|
| `bingAccountName`          | Unique name for the Bing grounding resource                       |
| `bingSku`                  | Pricing tier (e.g., `S1`)                                         |
| `connectionName`           | Name for the AML connection to Bing                               |
| `bingTargetEndpoint`       | Bing API endpoint (defaults to `https://api.bing.microsoft.com/`) |
| `tripadvisor_connection_id`| Azure connection ID for the TripAdvisor OpenAPI tool key          |
| `isSharedToAll`            | Whether the connection is shared with all users                   |

## Sample Data Instructions
This repo contains a `sample_data/` directory with:
- Sample user travel queries
- Example travel agent responses (mocked for offline testing)

You can test the interaction by invoking the agent with prompts like:

## Example Agent Interaction

#### 🧑 User:
Hey, I’m visiting Mountain View this weekend with my partner. We like nature, good coffee, and local food. Can you suggest things to do?

#### 🤖 Travel Agent:
Sure! Based on Bing and Tripadvisor, here are a few local highlights:
- **Shoreline Park**: Great for kayaking, biking, and birdwatching.
- **Red Rock Coffee** and **Verve Coffee Roasters** are top-rated cafés downtown.
- For food, **Eureka!** (gourmet burgers) and **Steins Beer Garden** (modern American) are local favorites.

Would you like me to find availability for kayaking at Shoreline?

#### 🧑 User:
Kayaking sounds fun! Can you check if it's available Saturday morning?

#### 🤖 Travel Agent:
Yes — according to Shoreline Lake's site via Bing, kayaking is available starting 10 AM on Saturday. 

## Customization Tips
- Modify the system instructions in `template.py` to enable the agent to provide the best responses as needed.
- Extend the agent with other useful tools or APIs (using OpenAPI spec) such as getting live flight details.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
