param projectPrincipalId string
param azureStorageName string
param projectWorkspaceId string

@description('Role Definition ID for Storage Blob Data Owner')
var storageBlobDataOwnerRoleId = 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b'

@description('Name of the container to assign the role')
var agentContainerName = '${projectWorkspaceId}-azureml-agent'

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-05-01' existing = {
  name: azureStorageName
}
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2022-05-01' existing = {
  parent: storageAccount
  name: 'default' // Blob service is always named 'default'
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2022-05-01' existing = {
  name: agentContainerName
  parent: blobService
}

resource storageBlobDataOwnerAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: blobContainer
  name: guid(blobContainer.id, storageBlobDataOwnerRoleId, projectPrincipalId)
  properties: {
    principalId: projectPrincipalId
    roleDefinitionId: storageBlobDataOwnerRoleId
    principalType: 'ServicePrincipal'
  }
}

