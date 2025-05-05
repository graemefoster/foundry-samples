# Azure AI Agent Service: Standard Agent Setup 1RP with Public Networking

> **NOTE:** This template is to set-up a network secured Standard Agent in AI Foundry. Includes: 
* PNA disabled resources
* PE's to all resources
* network injection enabled for Agents
* Deploy a VM for the user

## Steps 

See Instructions: https://microsoft-my.sharepoint.com/:w:/p/fosteramanda/ES-0A2WpCgVLrK3SH_7gT9YBBb8SZk639kKmU1AIpoeDJg?e=npAZWP


1. Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location westus
```

2. Deploy the template

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main.bicep
```
