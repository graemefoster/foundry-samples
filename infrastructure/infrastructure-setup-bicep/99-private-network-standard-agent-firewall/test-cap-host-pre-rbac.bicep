param principalId string


@description('Name of the AI Search resource')
param cosmosDBName string = 'grfcosmosstg'

resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = {
  name: cosmosDBName
  scope: resourceGroup()
}

resource cosmosDBOperatorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '230815da-be43-4aae-9cb4-875f7bd000aa'
  scope: resourceGroup()
}

resource cosmosDBOperatorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: cosmosDBAccount
  name: guid(principalId, cosmosDBOperatorRole.id, cosmosDBAccount.id)
  properties: {
    principalId: principalId
    roleDefinitionId: cosmosDBOperatorRole.id
    principalType: 'ServicePrincipal'
  }
}

// Reference existing storage account
resource storage 'Microsoft.Storage/storageAccounts@2022-05-01' existing = {
  name: 'grfteststg'
  scope: resourceGroup()
}

var projectWorkspaceId = '7b8492aaff794d1b9598128f3d05b07c'

module weird './modules-network-secured/format-project-workspace-id.bicep' = {
  name: 'formatWorkspaceId'
  params: {
    projectWorkspaceId: projectWorkspaceId
  }
}

resource searchService 'Microsoft.Search/searchServices@2024-06-01-preview' existing = {
  name: 'grfsearchtest'
  scope: resourceGroup()
}

// search roles
resource searchIndexDataContributorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
  scope: resourceGroup()
}

resource searchIndexDataContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: searchService
  name: guid(principalId, searchIndexDataContributorRole.id, searchService.id)
  properties: {
    principalId: principalId
    roleDefinitionId: searchIndexDataContributorRole.id
    principalType: 'ServicePrincipal'
  }
}

resource searchServiceContributorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
  scope: resourceGroup()
}

resource searchServiceContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: searchService
  name: guid(principalId, searchServiceContributorRole.id, searchService.id)
  properties: {
    principalId: principalId
    roleDefinitionId: searchServiceContributorRole.id
    principalType: 'ServicePrincipal'
  }
}

// Blob Storage Owner: b7e6dc6d-f1e8-4753-8033-0f276bb0955b
// Blob Storage Contributor: ba92f5b4-2d11-453d-a403-e96b0029c9fe
resource storageBlobDataContributor 'Microsoft.Authorization/roleDefinitions@2022-05-01-preview' existing = {
  name: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  scope: resourceGroup()
}

resource storageBlobDataContributorRoleAssignmentProject 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storage
  name: guid(principalId, storageBlobDataContributor.id, storage.id)
  properties: {
    principalId: principalId
    roleDefinitionId: storageBlobDataContributor.id
    principalType: 'ServicePrincipal'
  }
}
