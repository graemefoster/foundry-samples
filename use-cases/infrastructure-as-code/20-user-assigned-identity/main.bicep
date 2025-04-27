/*
  AI Foundry account and project - with your User-Assigned managed identity.
  
  Description: 
  - Create an AI Foundry (previously known as Azure AI Services) account and project with UAI.
  - Create a gpt-4o model deployment
  - When creating a project, the Identity is not updateable. Please select 'SystemAssigned', 'UserAssigned' or 'SystemAssigned,UserAssigned' during creation as this cannot be updated. .
  - Creating your first project is needed to support more capabilities and is the default reoute for APIs if no paramter is provided.

*/
@description('That name is the name of our application. It has to be unique. Type a name followed by your resource group name. (<name>-<resourceGroupName>)')
param aiServicesName string = 'aiServices-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the first project')
param defaultProjectName string = '${aiServicesName}-proj'
param defaultProjectDisplayName string = 'Project'
param defaultProjectDescription string = 'Describe what your project is about.'

/*
  Step 1: Get your existing/previously created Managed Identity

*/ 
@description('User Assigned Identity Name')
param userAssignedIdentityName string
@description('User Assigned Identity Resource Group Name')
param userIdentityResourceGroupName string = resourceGroup().name

var userAssignedIdentityId = extensionResourceId(format('/subscriptions/{0}/resourceGroups/{1}', subscription().subscriptionId, '${userIdentityResourceGroupName}'), 'Microsoft.ManagedIdentity/userAssignedIdentities', '${userAssignedIdentityName}')

/*
  Step 2: Create a Cognitive Services Account 

*/ 
resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiServicesName
  location: location
  identity: {
    type: 'SystemAssigned,UserAssigned' // Select 'UserAssigned' or 'SystemAssigned,UserAssigned' during creation as this cannot be updated.
    userAssignedIdentities: {
      '${userAssignedIdentityId}': {}
    }
  }
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    // Networking
    publicNetworkAccess: 'Enabled'

    // Specifies wheether this resource support project management as child resources, used as containers for access management, data isolation, and cost in AI Foundry.
    allowProjectManagement: true

    // Auth
    disableLocalAuth: true
  }
}

/*
  Step 3: Deploy gpt-4o model
  
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
  Step 4: Create a Project

*/
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: defaultProjectName
  parent: account
  location: location
  
  identity: {
    type: 'SystemAssigned,UserAssigned' // Select 'UserAssigned' or 'SystemAssigned,UserAssigned' during creation as this cannot be updated.
    userAssignedIdentities: {
    '${userAssignedIdentityId}': {}
    }
  }
  
  properties: {
    displayName: defaultProjectDisplayName
    description: defaultProjectDescription
    isDefault: true // can't be updated after creation; can only be set by one project in the account, the first project created.
  }
}

output accountId string = account.id
output accountName string = account.name
output project string = project.name
