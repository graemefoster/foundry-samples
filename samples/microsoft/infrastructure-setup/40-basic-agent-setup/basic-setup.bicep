param accountName string = 'basicaccount${substring(uniqueString(utcNow()), 0,4)}'
param projectName string = 'project'
param projectDescription string = 'some description'
param projectDisplayName string = 'project_display_name'
param location string = resourceGroup().location

param modelName string = 'gpt-4o'
param modelFormat string = 'OpenAI'
param modelVersion string = '2024-11-20'
param modelSkuName string = 'GlobalStandard'
param modelCapacity int = 30


#disable-next-line BCP081
resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: accountName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: toLower(accountName)
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: true
  }
}

/*
  Step 2: Deploy gpt-4o model
  
  - Agents will use the build-in model deployments
*/ 



/*
  Step 3: Create a Cognitive Services Project
    
*/
#disable-next-line BCP081
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: account
  name: projectName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: projectDescription
    displayName: projectDisplayName
  }
}

#disable-next-line BCP081
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01'= {
  parent: account
  name: modelName
  sku : {
    capacity: modelCapacity
    name: modelSkuName
  }
  properties: {
    model:{
      name: modelName
      format: modelFormat
      version: modelVersion
    }
  }
}

output account_name string = account.name
output project_name string = project.name
