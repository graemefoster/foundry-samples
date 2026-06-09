// Assigns Application Insights Reader role to the AI project managed identity.
// This supports running Evaluations on existing traces.

@description('Application Insights resource name')
param appInsightsName string

@description('Principal ID of the AI project managed identity')
param projectPrincipalId string

// Log Analytics Reader: 73c42c96-874c-492b-b04d-ab87d138a893
resource logAnalyticsReaderRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '73c42c96-874c-492b-b04d-ab87d138a893'
  scope: resourceGroup()
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightsName
}

resource appInsightsReaderAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: appInsights
  name: guid(projectPrincipalId, logAnalyticsReaderRole.id, appInsights.id)
  properties: {
    principalId: projectPrincipalId
    roleDefinitionId: logAnalyticsReaderRole.id
    principalType: 'ServicePrincipal'
  }
}
