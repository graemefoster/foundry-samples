/*
  Azure AI Fouondry accoutn and project - with Customer Managed Key (CMK)
  
  Description: 
  - Create an Azure AI Foundry account and project with CMK
  - Create a model deployment

*/
@description('That name is the name of our application. It has to be unique.Type a name followed by your resource group name. (<name>-<resourceGroupName>)')
param aiServicesName string = 'aiServices-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the first project')
param defaultProjectName string = '${aiServicesName}-proj'
param defaultProjectDisplayName string = 'Project'
param defaultProjectDescription string = 'Describe what your project is about.'

// Azure Key Vault
// These parameters are used under the encryption section of the Cognitive Services Account resource
@description('Name of the customers existing Azure Key Vault resource')
param azureKeyVaultName string
@description('Name of the Azure Key Vault target')
param azureKeyVaultTarget string = 'https://${azureKeyVaultName}.vault.azure.net/' 
@description('Resource Group name of the Azure Key Vault resource')
param azureKeyVaultResourceGroupName string = resourceGroup().name
@description('Subscription ID of the Azure Key Vault resource')
param azureKeyVaultSubscriptionId string = subscription().subscriptionId
@description('Name of the Azure Key Vault key')
param azureKeyName string
@description('Version of the Azure Key Vault key')
param azureKeyVersion string

/*
  Step 2: Create a Cognitive Services Account 
  
*/ 
resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiServicesName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    // Networking
    publicNetworkAccess: 'Disabled'

    // Encryption
    /*
    encryption: {
      keySource: 'Microsoft.KeyVault'
      keyVaultProperties: {
        keyName: azureKeyName
        keyVaultUri: azureKeyVaultTarget
        keyVersion: azureKeyVersion
      }
    }
    */

    // When set, we provision hub virtual workspace on existing Account
    // Below property cannot be reversed once set
    allowProjectManagement: true

    // auth
    disableLocalAuth: false
  }
}

/*
  Step 3: Deploy gpt-4o model
  
  - Agents will use the build-in model deployments
*/
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: account
  name: 'gpt-4o'
  sku : {
    capacity: 1
    name: 'GlobalStandard'
  }
  properties: {
    model:{
      name: 'gpt-4o'
      format: 'OpenAI'
      version: '2024-08-06'
    }
  }
}

/*
  Step 5: Create a Project. This resource maps to virtual Azure ML project

*/
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: defaultProjectName
  parent: account
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: defaultProjectDisplayName
    description: defaultProjectDescription

    isDefault: true //can't be updated after creation; can only be set by one project in the account
  }
}

output accountId string = account.id
output accountName string = account.name
output project string = project.name
