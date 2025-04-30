/*
This example demonstrates how to add an Azure AI Search connection.
*/
param aiFoundryName string = 'your-account'
param aiSearchName string = 'ais-${aiFoundryName}'

// whether ai Search is existing or new
@allowed([
  'new'
  'existing'
])
param newOrExisting string = 'new'
 
#disable-next-line BCP081
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aiFoundryName
  scope: resourceGroup()
}

resource existingSearchService 'Microsoft.Search/searchServices@2025-02-01-preview' existing = if (newOrExisting == 'existing') {
  name: aiSearchName
}

resource newSearchService 'Microsoft.Search/searchServices@2025-02-01-preview' = if (newOrExisting == 'new') {
  name: aiSearchName
  location: 'westus'
  sku: {
    name: 'basic'
  }
  properties: {}
}

resource project_connection_azureai_search 'Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview' = {
  name: aiSearchName
  parent: aiFoundry
  properties: {
    category: 'CognitiveSearch'
    target: ((newOrExisting == 'new') ? newSearchService.properties.endpoint : existingSearchService.properties.endpoint)
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: { 
      key: ((newOrExisting == 'new') ? listKeys(newSearchService.id, '2020-06-10').key1 : listKeys(existingSearchService.id, '2020-06-10').key1)
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: ((newOrExisting == 'new') ? newSearchService.id : existingSearchService.id)
      location: ((newOrExisting == 'new') ? newSearchService.location : existingSearchService.location)
    }
  }
}
