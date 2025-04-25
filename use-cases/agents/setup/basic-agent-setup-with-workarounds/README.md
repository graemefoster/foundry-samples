# Azure AI Agent Service: Basic Setup 1RP

## Basic Agent Setup - With Workarounds!

> **NOTE:** This template automatically performs the following workarounds:
>
> 1. Assign the project system managed identity (SMI) the following role ‘Azure AI Developer’ on its parent AI Services resource


This bicep template provisions required resources for a basic project setup. A new Cognitive Services Account is created, a gpt-4o model is deployed, and a new project is created.

All agents created in this project will automatically use Microsoft managed, multitenant search and storage resources.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fscenarios%2Fagents%2Fsetup%2Fbasic-agent-setup-with-workarounds%2Fazuredeploy.json)

To deploy this template, click the "Deploy to Azure" button or you can run one of the following commands

* Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location westus2
```

* Deploy the template

```bash
    az deployment group create --resource-group <new-rg-name> --template-file basic-setup.bicep
```
