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
# Deploy an Azure AI Foundry project with Customer Managed Keys

![Azure Public Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/PublicLastTestDate.svg)
![Azure Public Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/PublicDeployment.svg)

![Azure US Gov Last Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/FairfaxLastTestDate.svg)
![Azure US Gov Last Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/FairfaxDeployment.svg)

![Best Practice Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/BestPracticeResult.svg)
![Cred Scan Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/CredScanResult.svg)
![Bicep Version](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-cmk/BicepVersion.svg)

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fandyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-cmk%2Fazuredeploy.json)
[![Deploy To Azure US Gov](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazuregov.svg?sanitize=true)](https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fandyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-cmk%2Fazuredeploy.json)
[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2andyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-cmk%2Fazuredeploy.json)

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