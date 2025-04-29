# Azure AI Agent Service: Basic Setup 1RP

## Basic Agent Setup
   

This bicep template provisions required resources for a basic project setup. A new Cognitive Services Account is created, a gpt-4o model is deployed, and a new project is created.

All agents created in this project will automatically use Microsoft managed, multitenant search and storage resources.

### Prerequisites
1. To deploy the template, you must have the following roles:
    * Cognitive Services Contributor or Contributor 
1. To create your first agent you must have the permissions: Azure AI Developer and Cognitive Services User
 
### Steps

1. To deploy this template, click the "Deploy to Azure" button or you can run one of the following commands:


* Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location eastus
```

* Deploy the template

```bash
    az deployment group create --resource-group <new-rg-name> --template-file basic-setup.bicep
```
