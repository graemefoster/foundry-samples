# Azure AI Agent Service: Basic Setup using an existing Azure OpenAI resource for model deployments

## Basic Agent Setup using an existing AOAI resource for model deployments
   

This bicep template provisions required resources for the basic project setup. A new Cognitive Services Account and project are created. Your existing Azure OpenAI resource will be used for deployments. This template will create a project connection to your existing Azure OpenAI resource. 

> **Important:** You must pass in the **resource ID** of your existing Azure OpenAI resource when deploying this template.

All agents created in this project will automatically use Microsoft managed, multitenant search and storage resources.

### Prerequisites
1. To deploy the template, you must have the following roles:
    * Cognitive Services Contributor or Contributor 
1. To create your first agent you must have the permissions: Azure AI Developer and Cognitive Services User
 
### Steps

1. To deploy this template, click the "Deploy to Azure" button or you can run one of the following commands:

- Ensure you pass in the resourceId of your existing Azure OpenAI resource
    param existingAoaiResourceId = '/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group-name>/providers/Microsoft.CognitiveServices/accounts/<your-aoai-name>'

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F42-basic-agent-setup-use-existing-azureopenai%2Fmain.json)


* Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location eastus
```

* Deploy the template and edit the main.bicep file to include the resource ID of your Azure OpenAI resource

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main.bicep
```
