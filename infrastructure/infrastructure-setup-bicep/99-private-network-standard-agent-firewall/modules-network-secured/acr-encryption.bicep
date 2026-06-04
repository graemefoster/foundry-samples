// Updates ACR with CMK encryption after RBAC is assigned

@description('Name of the ACR')
param acrName string

@description('Location for the resource')
param location string

@description('Key Vault key URI (without version) for CMK encryption')
param keyVaultKeyUri string

resource existingAcr 'Microsoft.ContainerRegistry/registries@2025-11-01' existing = {
  name: acrName
}

resource acrUpdate 'Microsoft.ContainerRegistry/registries@2025-11-01' = {
  name: existingAcr.name
  location: location
  sku: {
    name: 'Premium'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    encryption: {
      status: 'enabled'
      keyVaultProperties: {
        keyIdentifier: keyVaultKeyUri
        identity: existingAcr.identity.principalId
      }
    }
  }
}
