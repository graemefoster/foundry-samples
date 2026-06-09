var foundryName = 'grfnetworktest7'
var subnetId = '/subscriptions/b045f4eb-724b-4361-80ff-2a0ff999a996/resourceGroups/foundrynetworked/providers/Microsoft.Network/virtualNetworks/grffoundrytest/subnets/newtest1'

resource foundry 'Microsoft.CognitiveServices/accounts@2026-01-15-preview' = {
  name: foundryName
  location: 'australiaeast'
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: foundryName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: [
        {
          value: '49.192.23.85'
        }
      ]
      bypass: 'AzureServices'
    }
    publicNetworkAccess: 'Enabled'

    networkInjections: [
      {
        scenario: 'agent'
        subnetArmId: subnetId
        useMicrosoftManagedNetwork: false
      }
    ]
    // Set disable local auth to true or false. Agent service does not support API key based authentication
    disableLocalAuth: false
    restrictOutboundNetworkAccess: false
  }
}

resource foundryProject 'Microsoft.CognitiveServices/accounts/projects@2026-03-01' = {
  name: 'proj-test-comparison'
  parent: foundry
  location: 'australiaeast'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    displayName: 'Project test'
    description: 'This is project test'
  }
  dependsOn: []
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2025-11-01-preview' existing = {
  name: 'grfcosmosstg'
}

resource account_connection_cosmosdb_account 'Microsoft.CognitiveServices/accounts/connections@2026-03-01' = {
  parent: foundry
  name: cosmos.name
  properties: {
    category: 'CosmosDB'
    target: cosmos.properties.documentEndpoint
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: cosmos.id
      location: cosmos.location
    }
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' existing = {
  name: 'grfteststg'
}

resource stg_connection 'Microsoft.CognitiveServices/accounts/connections@2026-03-01' = {
  parent: foundry
  name: storageAccount.name
  properties: {
    category: 'AzureStorageAccount'
    target: storageAccount.properties.primaryEndpoints.blob
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: storageAccount.id
      location: storageAccount.location
    }
  }
}

resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' existing = {
  name: 'grfsearchtest'
  scope: resourceGroup()
}

resource project_connection_azureai_search 'Microsoft.CognitiveServices/accounts/connections@2026-03-01' = {
  name: searchService.name
  parent: foundry
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${searchService.name}.search.windows.net'
    authType: 'AAD'
    metadata: {
      ApiType: 'Azure'
      ResourceId: searchService.id
      location: searchService.location
    }
  }
}

@description('Principal ID of the AI project')
var projectPrincipalId string = foundryProject.identity.principalId

module rbac1 'test-cap-host-pre-rbac.bicep' = {
  name: 'rbac1'
  params: {
    principalId: projectPrincipalId
  }
  dependsOn: [
    account_connection_cosmosdb_account
    stg_connection
    project_connection_azureai_search
  ]
}

resource foundryProjectCapHost 'Microsoft.CognitiveServices/accounts/projects/capabilityHosts@2026-03-01' = {
  name: 'caphost'
  parent: foundryProject
  properties: {
    threadStorageConnections: [cosmos.name]
    storageConnections: [storageAccount.name]
    vectorStoreConnections: [searchService.name]
  }
  dependsOn: [
    rbac1
  ]
}

module rbac3 'test-cap-host-post-rbac.bicep' = {
  name: 'rbac3'
  params: {
    principalId: projectPrincipalId
  }
  dependsOn: [
    foundryProjectCapHost
  ]
}


//tools don't work without connections in project cap-host
//but hosted agent seems to work....
