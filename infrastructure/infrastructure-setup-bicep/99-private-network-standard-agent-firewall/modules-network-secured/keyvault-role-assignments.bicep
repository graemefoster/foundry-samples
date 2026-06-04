// Assigns Key Vault Crypto Service Encryption User role to service identities for CMK

@description('Name of the Key Vault')
param keyVaultName string

@description('Principal ID of the AI Services account (SystemAssigned)')
param aiServicesPrincipalId string

@description('Principal ID of the Storage Account (SystemAssigned) - empty if BYO resource')
param storagePrincipalId string

@description('Principal ID of the AI Search service (SystemAssigned) - empty if BYO resource')
param aiSearchPrincipalId string

@description('Principal ID of the ACR (SystemAssigned)')
param acrPrincipalId string

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

// Key Vault Crypto Service Encryption User: e147488a-f6f5-4113-8e2d-b22465e65bf6
resource kvCryptoServiceEncryptionUserRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'e147488a-f6f5-4113-8e2d-b22465e65bf6'
  scope: resourceGroup()
}

// AI Services
resource aiServicesRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: keyVault
  name: guid(aiServicesPrincipalId, kvCryptoServiceEncryptionUserRole.id, keyVault.id)
  properties: {
    principalId: aiServicesPrincipalId
    roleDefinitionId: kvCryptoServiceEncryptionUserRole.id
    principalType: 'ServicePrincipal'
  }
}

// Storage Account (skipped if BYO resource with empty principal ID)
resource storageRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(storagePrincipalId)) {
  scope: keyVault
  name: guid(storagePrincipalId, kvCryptoServiceEncryptionUserRole.id, keyVault.id)
  properties: {
    principalId: storagePrincipalId
    roleDefinitionId: kvCryptoServiceEncryptionUserRole.id
    principalType: 'ServicePrincipal'
  }
}

// AI Search (skipped if BYO resource with empty principal ID)
resource aiSearchRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(aiSearchPrincipalId)) {
  scope: keyVault
  name: guid(aiSearchPrincipalId, kvCryptoServiceEncryptionUserRole.id, keyVault.id)
  properties: {
    principalId: aiSearchPrincipalId
    roleDefinitionId: kvCryptoServiceEncryptionUserRole.id
    principalType: 'ServicePrincipal'
  }
}

// ACR
resource acrRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: keyVault
  name: guid(acrPrincipalId, kvCryptoServiceEncryptionUserRole.id, keyVault.id)
  properties: {
    principalId: acrPrincipalId
    roleDefinitionId: kvCryptoServiceEncryptionUserRole.id
    principalType: 'ServicePrincipal'
  }
}
