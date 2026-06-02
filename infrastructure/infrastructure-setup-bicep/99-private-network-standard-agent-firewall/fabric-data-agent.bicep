/*
Common module for creating ModelGateway connections to Azure AI Foundry projects.
This module handles the core connection logic and can be reused across different ModelGateway connection samples.
ModelGateway connections support ApiKey and Oauth2.0 client credentials authentication.
*/

// Project resource parameters
//        <set-backend-service base-url="https://management.azure.com/subscriptions/b045f4eb-724b-4361-80ff-2a0ff999a996/resourceGroups/PublicFoundry/providers/Microsoft.CognitiveServices/accounts/grfpublicfoundryaueast" />

var projectResourceId string = '/subscriptions/b045f4eb-724b-4361-80ff-2a0ff999a996/resourceGroups/PublicFoundry/providers/Microsoft.CognitiveServices/accounts/grfpublicfoundryaueast/projects/proj-default'

// Extract project information from resource ID
var aiFoundryName = split(projectResourceId, '/')[8]
var projectName = split(projectResourceId, '/')[10]

// Reference the AI Foundry account
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aiFoundryName
  scope: resourceGroup()
}

// Reference the project within the AI Foundry account
resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  name: projectName
  parent: aiFoundry
}

resource testFakeFabric 'Microsoft.CognitiveServices/accounts/projects/connections@2025-10-01-preview' = {
  name: 'fabric-connection'
  parent: aiProject
  properties: {
    category: 'CustomKeys'
    authType: 'CustomKeys'
    credentials: {
      keys: {
        'workspace-id': 'bc05ce49-a9e2-425f-bc94-30fd7464671c'
        'artifact-id': 'd254f8d2-1459-4c1b-b5e0-205ae8ec9d1d'
      }
    }
    metadata: {
      type: 'fabric_dataagent_preview'
    }
  }
}

