// Assigns ACR repository read access to the AI project managed identity

@description('Azure Container Registry resource name')
param acrName string

@description('Principal ID of the AI project managed identity')
param projectPrincipalId string

// Container Registry Repository Reader: b93aa761-3e63-49ed-ac28-beffa264f7ac
resource acrRepositoryReaderRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'b93aa761-3e63-49ed-ac28-beffa264f7ac'
  scope: resourceGroup()
}

resource acr 'Microsoft.ContainerRegistry/registries@2025-11-01' existing = {
  name: acrName
}

resource acrRepositoryReaderRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: acr
  name: guid(projectPrincipalId, acrRepositoryReaderRole.id, acr.id)
  properties: {
    principalId: projectPrincipalId
    roleDefinitionId: acrRepositoryReaderRole.id
    principalType: 'ServicePrincipal'
  }
}
