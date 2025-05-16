# Azure AI Agent Service: Standard Agent Setup 1RP with Private E2E Networking 

> **NOTE:** This template is to set-up a network secured Standard Agent in AI Foundry. Includes: 
* PNA disabled resources
* PE's to all resources
* Network injection enabled for Agents

## Steps 

1. Create new (or use existing) resource group:

```bash
    az group create --name <new-rg-name> --location westus
```

2. Deploy the main-create.bicep

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main-create.bicep
```
3. Run the CheckCapabilityHostReadiness.ps1 and edit the command to add your subscription ID, resource group name, and your newly deployed AI Services account resource name.

```bash
    .\CheckCapabilityHostReadiness.ps1 -subscriptionId "<your-sub-id>" -resourcegroup "<new-rg-name>" -accountname "<your-aiservices-name>"
```

4. Deploy the main-project-caphost-create.bicep

```bash
    az deployment group create --resource-group <new-rg-name> --template-file main-project-caphost-create.bicep.bicep
```

**NOTE:** To access your Foundry resource securely, please using either a VM, VPN, or ExpressRoute.