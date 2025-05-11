/*
  AI Foundry using Customer Managed Keys (CMK) for data encryption
  
  Description: 
  - Create an Azure AI Foundry account 
  - Create a project
  - Create a model deployment
  
  Important: Agent APIs do not support customer-managed key encryption in basic setup. 
  To use customer-managed key encryption with Agents, you must bring your own storage
  resources using 'standard' agent setup. Also, see example 31.
*/
@description('That name is the name of our application. It has to be unique. Type a name followed by your resource group name. (<name>-<resourceGroupName>)')
param aiFoundryName string = 'youraifoundry'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the Azure Key Vault target')
param keyVaultName string = 'mykeyvault'

@description('Name of the Azure Key Vault key')
param keyName string = 'key'

@description('Version of the Azure Key Vault key')
param keyVersion string = 'ae6749b47c2a4a68aa60d4c14580d5c6'

var keyVaultUri = 'https://${keyVaultName}.vault.azure.net/'

/*
  An AI Foundry resources is a variant of a CognitiveServices/account resource type
*/ 
resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiFoundryName
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

    // Set to use with AI Foundry
    allowProjectManagement: true

    // Enable EntraID and disable key-based auth. Note that some AI Foundry features only support EntraID.
    customSubDomainName: aiFoundryName
    disableLocalAuth: false
  }
}

// Set up customer-managed key encryption once managed identity has been created
module encryptionUpdate 'updateEncryption.bicep' = {
  name: 'updateEncryption'
  params: {
    aiFoundryName: account.name
    aiFoundryPrincipal: account.identity.principalId
    keyVaultName: keyVaultName
    location: location
    keyVaultUri: keyVaultUri
    keyName: keyName
    keyVersion: keyVersion
  }
}

/*
  Developer APIs are exposed via a project, which groups in- and outputs that relate to one use case, including files.
  Its advisable to create one project right away, so development teams can directly get started.
  Projects may be granted individual RBAC permissions and identities on top of what account provides.
*/ 
// resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
//   name: 'myproject'
//   parent: account
//   location: location
//   identity: {
//     type: 'SystemAssigned'
//   }
//   properties: {
//     displayName: 'myproject'
//     description: 'mydescription'
//     isDefault: true //can't be updated after creation; can only be set by one project in the account
//   }
// }

/*
  Optionally deploy a model to use in playground, agents and other tools.
*/
// resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
//   parent: account
//   name: 'gpt-4o-mini'
//   sku : {
//     capacity: 1
//     name: 'GlobalStandard'
//   }
//   properties: {
//     model:{
//       name: 'gpt-4o'
//       format: 'OpenAI'
//       version: '2024-08-06'
//     }
//   }
// }

output accountId string = account.id
output accountName string = account.name
//output project string = project.name
