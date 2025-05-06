/*
Connections enable your AI applications to access tools and objects managed elsewhere in or outside of Azure.

This example demonstrates how to add an Azure Application Insights connection.

Only one application insights can be set on a project at a time.
*/
param aiFoundryName string = '<your-foundry-name>'
param connectedResourceName string = 'st${aiFoundryName}'
param location string = 'westus'

// Whether to create a new Azure AI Search resource
@allowed([
  'new'
  'existing'
])
param newOrExisting string = 'new'
 
// Refers your existing Azure AI Foundry resource
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aiFoundryName
  scope: resourceGroup()
}

// Conditionally refers your existing Azure AI Search resource
resource existingStorage 'Microsoft.Storage/storageAccounts@2024-01-01' existing = if (newOrExisting == 'existing') {
  name: connectedResourceName
}

// Conditionally creates a new Azure AI Search resource
resource newStorage 'Microsoft.Storage/storageAccounts@2024-01-01' = if (newOrExisting == 'new') {
  name: connectedResourceName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// Creates the Azure Foundry connection to your Azure App Insights resource
resource connection 'Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview' = {
  name: '${aiFoundryName}-storage'
  parent: aiFoundry
  properties: {
    category: 'AzureStorageAccount'
    target: ((newOrExisting == 'new') ? newStorage.id : existingStorage.id)
    authType: 'AccountKey'
    credentials: {
      key: string((newOrExisting == 'new') ? newStorage.listKeys().keys : existingStorage.listKeys().keys)
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: ((newOrExisting == 'new') ? newStorage.id : existingStorage.id)
    }
  }
}
