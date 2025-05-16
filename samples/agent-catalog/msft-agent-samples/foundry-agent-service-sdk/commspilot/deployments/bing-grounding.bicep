param account_name string
param location string = 'global'
var bingSearchName = 'bingsearch-${account_name}'

resource accountResource 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: account_name
  scope: resourceGroup()
}

resource bingSearch 'Microsoft.Bing/accounts@2020-06-10' = {
  name: bingSearchName
  location: location
  sku: {
    name: 'G1'
  }
  kind: 'Bing.Grounding'
}

resource bingConnection 'Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview' = {
  name: '${account_name}-bingsearchconnection'
  parent: accountResource
  properties: {
    category: 'ApiKey'
    target: 'https://api.bing.microsoft.com/'
    authType: 'ApiKey'
    credentials: {
      key: listKeys(bingSearch.id, '2020-06-10').key1
    }
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      Location: bingSearch.location
      ResourceId: bingSearch.id
    }
  }
}
