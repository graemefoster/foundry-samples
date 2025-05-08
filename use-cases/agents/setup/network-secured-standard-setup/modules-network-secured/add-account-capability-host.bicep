
param accountName string
param accountCapHost string

resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
   name: accountName
}

 resource accountCapabilityHost 'Microsoft.CognitiveServices/accounts/capabilityHosts@2025-04-01-preview' = {
   name: accountCapHost
   parent: account
   properties: {
     capabilityHostKind: 'Agents'
   
   }
}

output accountCapHost string = accountCapabilityHost.name
