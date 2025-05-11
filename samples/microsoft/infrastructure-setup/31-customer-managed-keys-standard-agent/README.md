---
description: This template deploys an Azure AI Foundry account, project, and model deployment while using your key for encryption (Customer Managed Key).
page_type: sample
products:
- azure
- azure-resource-manager
urlFragment: aifoundry-cmk
languages:
- bicep
- json
---
# Set up Azure AI Foundry using Customer Managed Keys for encryption

This Azure AI Foundry template is built on Azure Cognitive Services as a resource provider. This template deploys an Azure AI Foundry account and project.

Run the command for BICEP:

az deployment group create --name "{DEPLOYMENT_NAME}" --resource-group "{RESOURCE_GROUP_NAME}" --template-file ./main.bicep --parameters azureKeyVaultName="{KEY_VAULT_NAME}" azureKeyName="{KEY_NAME}" azureKeyVersion="{KEY_VERSION}"

Steps:
1. Run the command above once to create the account and project without CMK.
1. Give account resource Key Vault Admin role, or more restricted get/wrap/unwrap key role assignments, on the Azure Key Vault. 
1. Uncomment out the encryption section in the main.bicep file to update with CMK.

Limitations:
1. Account cannot be created with encryption block. Users must create, then update the account with the encryption block.
1. User-Assigned Managed Identity is not supported with Customer Managed Keys.

If you are new to Azure AI Foundry, see:

- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)

If you are new to template deployment, see:

- [Azure Resource Manager documentation](https://learn.microsoft.com/azure/azure-resource-manager/)
- [Azure AI services quickstart article](https://learn.microsoft.com/azure/cognitive-services/resource-manager-template)

`Tags: Microsoft.CognitiveServices/accounts/projects`


# Give CosmosDB appID access to your key vault
appid: a232010e-820c-4083-83bb-3ace5fc29d0b;
az cosmosdb update --name "<your-account>" --resource-group "<your-rgp>" --key-uri "https://<your-account>>.vault.azure.net/keys/<key>" --subscription "<subscription>"

# Enable encryption on Azure Search
az search service update --name "<your-search>" --resource-group "<your-rgp>" --encryption-key-uri "https://<your-account>.vault.azure.net/keys/<key>"
