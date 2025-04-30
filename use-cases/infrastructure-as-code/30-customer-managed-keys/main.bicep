/*
  AI Foundry using Customer Managed Keys (CMK) for data encryption
  
  Description: 
  - Create an Azure AI Foundry account 
  - Create a project
  - Create a model deployment
  
  Important: Agent APIs do not support customer-managed key encryption in basic setup. This requires 'standard' setup, where you bring your own storage resources. Refer to standard Agent setup examples.
*/
@description('That name is the name of our application. It has to be unique.Type a name followed by your resource group name. (<name>-<resourceGroupName>)')
param aiServicesName string = 'aiServices-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the first project')
param defaultProjectName string = '${aiServicesName}-proj'
param defaultProjectDisplayName string = 'Project'
param defaultProjectDescription string = 'Describe what your project is about.'

/*
  Reference your encryption key from an Azure Key Vault resource
*/ 
@description('Name of the customers existing Azure Key Vault resource')
param azureKeyVaultName string = 'es2euapdeeik'
@description('Name of the Azure Key Vault target')
param azureKeyVaultTarget string = 'https://${azureKeyVaultName}.vault.azure.net/' 
@description('Resource Group name of the Azure Key Vault resource')
param azureKeyVaultResourceGroupName string = resourceGroup().name
@description('Subscription ID of the Azure Key Vault resource')
param azureKeyVaultSubscriptionId string = subscription().subscriptionId
@description('Name of the Azure Key Vault key')
param azureKeyName string = 'es2euapdeeik'
@description('Version of the Azure Key Vault key')
param azureKeyVersion string = 'a1f7ef03275b48ad8612d279350607d7'

/*
  An AI Foundry resources is a variant of a CognitiveServices/account resource type
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

    // Encryption properties may only be set at update, after creation, in case of system-assigned managed identity since the identity must be created first.
    encryption: {
      keySource: 'Microsoft.KeyVault'
      keyVaultProperties: {
        keyName: azureKeyName
        keyVaultUri: azureKeyVaultTarget
        keyVersion: azureKeyVersion
      }
    }

    // When set, we provision hub virtual workspace on existing Account
    // Below property cannot be reversed once set
    allowProjectManagement: true

    // temporarily needed
    customSubDomainName: aiServicesName
    
    // auth
    disableLocalAuth: false
  }
}

/*
  Developer APIs are exposed via a project, which groups in- and outputs that relate to one use case, including files.
  Its advisable to create one project right away, so development teams can directly get started.
  Projects may be granted individual RBAC permissions and identities on top of what account provides.
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

/*
  Optionally deploy a model to use in playground, agents and other tools.
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

output accountId string = account.id
output accountName string = account.name
output project string = project.name
