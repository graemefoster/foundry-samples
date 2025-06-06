# Azure AI Agent Service: Basic Setup Using an Existing Azure OpenAI Resource

This Bicep template provisions the required resources for a basic agent project. It creates a new Cognitive Services Account and project, and connects your existing Azure OpenAI resource for model deployments.

> **Important:** You must provide the **resource ID** of your existing Azure OpenAI resource when deploying this template.

All agents created in this project will automatically use Microsoft-managed, multitenant search and storage resources.

---

## Prerequisites

1. **Azure Roles:**
   - To deploy the template: **Azure AI Account Owner** or **Contributor**
   - To create your first agent: **Azure AI User** 
2. **Existing Azure OpenAI Resource:**
   - You must have an existing Azure OpenAI resource. [Learn more](https://learn.microsoft.com/azure/ai-services/openai/overview)
---

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F42-basic-agent-setup-use-existing-azureopenai%2Fmain.json)

## Deployment Steps

### 1. Prepare Parameters

- Ensure you have the resource ID of your existing Azure OpenAI resource. You can get this in Azure Portal. Example:
  ```bicep
  param existingAoaiResourceId = '/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group-name>/providers/Microsoft.CognitiveServices/accounts/<your-aoai-name>'
  ```
  ![Azure BYO Example](./azurebyo.PNG)


* Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location eastus
```

* Deploy the template and edit the main.bicep file to include the resource ID of your Azure OpenAI resource

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main.bicep
```
