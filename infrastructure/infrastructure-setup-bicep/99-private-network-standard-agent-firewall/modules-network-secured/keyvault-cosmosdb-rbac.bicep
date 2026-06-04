// Assigns Key Vault Crypto Service Encryption User role to Cosmos DB first-party service principal
// This must run BEFORE Cosmos DB is created with keyVaultKeyUri

@description('Name of the Key Vault')
param keyVaultName string

@description('Object ID of the Cosmos DB first-party service principal in this tenant')
param cosmosDBServicePrincipalId string

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

// Key Vault Crypto Service Encryption User: e147488a-f6f5-4113-8e2d-b22465e65bf6
resource kvCryptoServiceEncryptionUserRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'e147488a-f6f5-4113-8e2d-b22465e65bf6'
  scope: resourceGroup()
}

resource cosmosDBRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: keyVault
  name: guid(cosmosDBServicePrincipalId, kvCryptoServiceEncryptionUserRole.id, keyVault.id)
  properties: {
    principalId: cosmosDBServicePrincipalId
    roleDefinitionId: kvCryptoServiceEncryptionUserRole.id
    principalType: 'ServicePrincipal'
  }
}
