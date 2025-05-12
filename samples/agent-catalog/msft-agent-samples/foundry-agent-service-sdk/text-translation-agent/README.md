# Translation Agent

## Summary
The **Translation Agent** is an AI-powered agent built using Azure AI Agent Service and Azure AI Translator. It helps handle multilingual text processing, including dynamic language detection and bidirectional translation using Azure AI Translator services.

## Use Cases
1. **Text Translation**: Translate text between multiple languages for seamless communication.
2. **Business Communication**: Enable businesses to localize content for global audiences.
3. **Educational Content**: Translate learning materials to make them accessible to non-native speakers.

## Architecture Overview
The system consists of:
- An AI Agent created with Azure AI Agent Service using `gpt-4o` as the base model.
- Azure AI Translator integrated for language detection and translation.
- A Bicep template to automate provisioning of Azure resources.

```text
+----------------+                         
|   User Query   |                         
| (Any Language) |                         
+-------+--------+                         
        |                                  
        v                                  
+-------------------+        invokes        +----------------------------+
| Translation Agent | ------------------->  | Azure AI Translator (API)  |
|     (AI Agent)    | <-------------------  | (Language Translation)     |
+-------------------+        results        +----------------------------+
        |                                  
        v                                  
+-------------------------------+           
| Agent Respond translated text |                   
+-------------------------------+           

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
    translation_api="<translation-api>"
     amlWorkspaceResourceName="<AI-Project-Name>"
```

4. **Run the Agent Script**
```bash
 python agent.py
```

## ⚙️ Configuration Guide
| Parameter Name                         | Description                                                     |
|----------------------------------------|-----------------------------------------------------------------|
| `amlWorkspaceResourceName`             | Name of the AI Project or the AML workspace                     |
| `translator_resource_connection_name`  | API endpoint to call translation service                        |
| `project_endpoint`                     | Endpoint for the project this agent is using                    |
| `model_name`                           | Name of the model to be used for the Agent                      |
| `connection_id`                        | Connection ID for the translation resource in the AI Foundry    |

## Sample Data Instructions
This repo contains a `sample_data/` directory with:
- Sample user translation queries
- However, you are welcome to translate your own text

You can test the interaction by invoking the agent with prompts like:
## Example Agent Interaction
### User: 
Translate this Chinese poem to English: 白日依山尽，黄河入海流

### Agent:
At the end of the day, the Yellow River flows into the sea.

### User: 
translate this text to Chinese, Spanish, and Korean: Translator Agent handles multilingual text processing, including dynamic language detection and bidirectional translation using Translator service. The translator agent is triggered when the user message has the “translation intent”.

### Agent: 
Here are the translations:

Chinese: Translator Agent 处理多语言文本，包括使用 Translator服务的动态语言检测和双向翻译。当用户消息具有 “translation intent” 时，将触发翻译代理。
Spanish: Translator Agent se encarga del procesamiento de texto multilingüe, incluida la detección dinámica de idiomas y la traducción bidireccional mediante el servicio Translator. El agente traductor se activa cuando el mensaje del usuario tiene la "intención de traducción".
Korean: Translator Agent는 Translator 서비스를 사용하여 동적 언어 감지 및 양방향 번역을 포함한 다국어 텍스트 처리를 처리합니다. 변환기 에이전트는 사용자 메시지에 "번역 의도"가 있을 때 트리거됩니다.

### User: 
localize this text to Japanese and Germany: The agent can detect the source language for the input text unless the source language is defined in the user message. 

### Agent: 
Here are the localized texts:

Japanese: エージェントは、入力テキストのソース言語を検出できます。ただし、ソース言語がユーザー・メッセージで定義されていない場合に限ります。
German: Der Agent kann die Ausgangssprache für den Eingabetext erkennen, es sei denn, die Ausgangssprache ist in der Benutzermeldung definiert.

## Customization Tips
- Modify the system instructions in `agent.py` to your specif needs (e.g., special handling on some terminologies).
- Extend the agent with other useful tools or APIs (using OpenAPI spec).

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.