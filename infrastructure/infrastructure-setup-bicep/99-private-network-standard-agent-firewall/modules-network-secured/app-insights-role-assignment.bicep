// Assigns Application Insights Reader role to the AI project managed identity.
// This supports running Evaluations on existing traces.

@description('Application Insights resource name')
param appInsightsName string

@description('Principal ID of the AI project managed identity')
param projectPrincipalId string

// Reader: acdd72a7-3385-48ef-bd42-f606fba81ae7
resource readerRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
  scope: resourceGroup()
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightsName
}

resource appInsightsReaderAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: appInsights
  name: guid(projectPrincipalId, readerRole.id, appInsights.id)
  properties: {
    principalId: projectPrincipalId
    roleDefinitionId: readerRole.id
    principalType: 'ServicePrincipal'
  }
}
