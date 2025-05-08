---
description: This template deploys an Azure AI Foundry account, project, and model deployment with your User-Assigned Managed Identity.
page_type: sample
products:
- azure
- azure-resource-manager
urlFragment: aifoundry-uai
languages:
- bicep
- json
---
# Deploy an Azure AI Foundry project

![Azure Public Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/PublicLastTestDate.svg)
![Azure Public Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/PublicDeployment.svg)

![Azure US Gov Last Test Date](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/FairfaxLastTestDate.svg)
![Azure US Gov Last Test Result](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/FairfaxDeployment.svg)

![Best Practice Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/BestPracticeResult.svg)
![Cred Scan Check](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/CredScanResult.svg)
![Bicep Version](https://azurequickstartsservice.blob.core.windows.net/badges/quickstarts/microsoft.cognitiveservices/aifoundry-uai/BicepVersion.svg)

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fandyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-uai%2Fazuredeploy.json)
[![Deploy To Azure US Gov](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazuregov.svg?sanitize=true)](https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fandyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-uai%2Fazuredeploy.json)
[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2andyaviles121%2Fazure-quickstart-templates%2Faifoundry-basic-projects%2Fquickstarts%2Fmicrosoft.cognitiveservices%2Faifoundry-uai%2Fazuredeploy.json)

This Azure AI Foundry template is built on Azure Cognitive Services as a resource provider. This template deploys an Azure AI Foundry account and project, previously known as Azure AI Services.

Run the command for BICEP:

az deployment group create --name "{DEPLOYMENT_NAME}" --resource-group "{RESOURCE_GROUP_NAME}" --template-file ./main.bicep --parameters  userAssignedIdentityName="{UASER_ASSIGNED_MANAGED_IDENTITY_NAME}" 

Limitations:
1. User-Assigned Managed Identity is not supported with Customer Managed Keys.

If you are new to Azure AI Foundry, see:

- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)

If you are new to template deployment, see:

- [Azure Resource Manager documentation](https://learn.microsoft.com/azure/azure-resource-manager/)
- [Azure AI services quickstart article](https://learn.microsoft.com/azure/cognitive-services/resource-manager-template)

`Tags: Microsoft.CognitiveServices/accounts/projects`