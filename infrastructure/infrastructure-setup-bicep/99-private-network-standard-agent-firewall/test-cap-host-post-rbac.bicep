param principalId string
var projectWorkspaceId = '7b8492aaff794d1b9598128f3d05b07c'


var userThreadName = '${projectWorkspaceId}-thread-message-store'

@description('Name of the AI Search resource')
param cosmosDBName string = 'grfcosmosstg'

resource cosmosDBAccount 'Microsoft.DocumentDB/databaseAccounts@2024-12-01-preview' existing = {
  name: cosmosDBName
  scope: resourceGroup()
}

// Reference existing database
resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-12-01-preview' existing = {
  parent: cosmosDBAccount
  name: 'enterprise_memory'
}

resource containerUserMessageStore 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-12-01-preview' existing = {
  parent: database
  name: userThreadName
}

var roleDefinitionId = resourceId(
  'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions',
  cosmosDBName,
  '00000000-0000-0000-0000-000000000002'
)

var accountScope = '/subscriptions/${subscription().subscriptionId}/resourceGroups/${resourceGroup().name}/providers/Microsoft.DocumentDB/databaseAccounts/${cosmosDBName}/dbs/enterprise_memory'

resource containerRoleAssignmentUserContainer 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2022-05-15' = {
  parent: cosmosDBAccount
  name: guid(projectWorkspaceId, containerUserMessageStore.id, roleDefinitionId, principalId)
  properties: {
    principalId: principalId
    roleDefinitionId: roleDefinitionId
    scope: accountScope
  }
}

module weird './modules-network-secured/format-project-workspace-id.bicep' = {
  name: 'formatWorkspaceId'
  params: {
    projectWorkspaceId: projectWorkspaceId
  }
}


// The Storage Blob Data Owner role must be assigned after the caphost is created
module storageContainersRoleAssignment 'modules-network-secured/blob-storage-container-role-assignments.bicep' = {
  name: 'storage-containers-ra-asdasdas-deployment'
  params: {
    aiProjectPrincipalId: principalId
    storageName: 'grfteststg'
    workspaceId: weird.outputs.projectWorkspaceIdGuid
  }
}
