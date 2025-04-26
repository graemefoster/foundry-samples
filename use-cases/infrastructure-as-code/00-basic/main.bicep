param aiServicesName string = 'myaiservices123'
param location string = 'East US 2'
param sku string = 'S0'
param aiProjectName string = 'myaiservices123-proj'

resource aiService 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: aiServicesName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: sku
  }
  kind: 'AIServices'
  properties: {
    allowProjectManagement: true
  }
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: aiProjectName
  parent: aiService
  location: location
  identity: {
    type: 'SystemAssigned'
  }
}
