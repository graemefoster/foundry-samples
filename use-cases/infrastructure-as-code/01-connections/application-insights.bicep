/*
This example demonstrates how to add an Azure Application Insights connection.

To learn more about using Application Insights for tracing in AI Foundry, see https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/trace.

Only one application insights can be set on a project at a time.
*/
param aifoundry_resource_name string = 'your-aifoundry-name'
param appinsights_resource_name string = 'appi-${aifoundry_resource_name}'

#disable-next-line BCP081
resource aifoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aifoundry_resource_name
  scope: resourceGroup()
}

#disable-next-line BCP081
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appinsights_resource_name
  location: 'westus'
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

#disable-next-line BCP081
resource application_insights_connection 'Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview' = {
  name: '${aifoundry_resource_name}-appinsights-connection'
  parent: aifoundry
  properties: {
    category: 'AppInsights'
    target: appInsights.id
    authType: 'ApiKey'
    credentials: {
      key: appInsights.properties.InstrumentationKey
    }
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      ResourceId: appInsights.id
    }
  }
}
