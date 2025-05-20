# Azure AI Agent Service: Standard Agent Setup 1RP with Public Networking

> **NOTE:** This template is now supported

## Steps

See Instructions: https://microsoft-my.sharepoint.com/:w:/p/fosteramanda/ES-0A2WpCgVLrK3SH_7gT9YBBb8SZk639kKmU1AIpoeDJg?e=npAZWP

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure-ai-foundry%2Ffoundry-samples%2Frefs%2Fheads%2Fmain%2Fsamples%2Fmicrosoft%2Finfrastructure-setup%2F41-standard-agent-setup%2Fazuredeploy.json)

1. Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location westus
```

2. Deploy the template

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main.bicep
```

## Use exitsing resources

**Azure Cosmos DB**
- Ensure your exitsing Cosmos DB resource has a total Total throughput limit of at least 60000 RU/s
    - 3 containers will be provisioned in your existing Cosmos DB account and each need 20,000 RU/s
