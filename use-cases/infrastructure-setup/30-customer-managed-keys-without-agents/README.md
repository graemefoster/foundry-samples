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
# Set up Azure AI Foundry with Customer Managed Keys for Encryption

This Azure AI Foundry template example demonstrates how to configure customer-managed key encryption on an AI Foundry resource.

Configuring customer managed keys is performed using a two-step approach, in which first the resource is created without encryption to allow the managed identity to be created. In a second step, the managed identity is assigned access to your key vault and encryption is applied on your resource.

Run the command for BICEP:

az deployment group create --name "{DEPLOYMENT_NAME}" --resource-group "{RESOURCE_GROUP_NAME}" --template-file ./main.bicep --parameters azureKeyVaultName="{KEY_VAULT_NAME}" azureKeyName="{KEY_NAME}" azureKeyVersion="{KEY_VERSION}"

Prerequisites:
1. An Azure Key Vault with an existing key, soft delete and purge protection enabled
