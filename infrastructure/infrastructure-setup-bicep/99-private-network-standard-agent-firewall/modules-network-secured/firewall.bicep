param firewallPipName string
param firewallMgmtPipName string
param firewallName string
param firewallPolicyName string
param location string = resourceGroup().location
param firewallSubnetId string
param firewallManagementSubnetId string
param logAnalyticsId string
param yarpProxyFqdn string

resource firewallPip 'Microsoft.Network/publicIPAddresses@2022-11-01' = {
  name: firewallPipName
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
  zones: pickZones('Microsoft.Network', 'publicIPAddresses', location, 3)
}

resource firewallManagementPip 'Microsoft.Network/publicIPAddresses@2022-11-01' = {
  name: firewallMgmtPipName
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
  zones: pickZones('Microsoft.Network', 'publicIPAddresses', location, 3)
}

resource fwallPolicy 'Microsoft.Network/firewallPolicies@2022-11-01' = {
  name: firewallPolicyName
  location: location
  properties: {
    sku: {
      tier: 'Basic'
    }
  }
}

resource firewall 'Microsoft.Network/azureFirewalls@2022-11-01' = {
  name: firewallName
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig'
        properties: {
          subnet: {
            id: firewallSubnetId
          }
          publicIPAddress: {
            id: firewallPip.id
          }
        }
      }
    ]
    sku: {
      name: 'AZFW_VNet'
      tier: 'Basic'
    }
    managementIpConfiguration: {
      name: 'mgmntipconfig'
      properties: {
        publicIPAddress: {
          id: firewallManagementPip.id
        }
        subnet: {
          id: firewallManagementSubnetId
        }
      }
    }
    firewallPolicy: {
      id: fwallPolicy.id
    }
  }
}

resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: firewall
  name: 'diagnostics'
  properties: {
    workspaceId: logAnalyticsId
    logs: [
      {
        categoryGroup: 'allLogs'
        enabled: true
      }
    ]
  }
}

resource policyRuleCollectionGroup 'Microsoft.Network/firewallPolicies/ruleCollectionGroups@2025-01-01' = {
  parent: fwallPolicy
  name: 'defaultRuleGroup'
  properties: {
    priority: 100
    ruleCollections: [
      // NAT rules (NAT collection)
      {
        name: 'Nat-DNAT-ManagementHttps'
        ruleCollectionType: 'FirewallPolicyNatRuleCollection'
        priority: 200
        action: {
          type: 'DNAT'
        }
        rules: [
          {
            ruleType: 'NatRule'
            name: 'DNAT-ManagementHttps'
            description: 'DNAT for management HTTPS'
            sourceAddresses: ['*']
            ipProtocols: ['TCP']
            destinationAddresses: [
              firewallPip.properties.ipAddress
            ]
            destinationPorts: ['443']
            translatedFqdn: yarpProxyFqdn
            translatedPort: '443'
          }
        ]
      }
      // Network rules (Filter collection)
      {
        name: 'Net-AllowAllNonHttpOut'
        ruleCollectionType: 'FirewallPolicyFilterRuleCollection'
        priority: 300
        action: {
          type: 'Allow'
        }
        rules: [
          {
            ruleType: 'NetworkRule'
            name: 'AllowAllNonHttpOut'
            description: 'Allow all outbound traffic except 80/443'
            sourceAddresses: ['*']
            destinationAddresses: ['*']
            destinationPorts: ['1-79', '81-442', '444-65535']
            ipProtocols: ['Any']
          }
        ]
      }
      // Application rules (Filter collection)
      {
        name: 'App-AllowWebOut'
        ruleCollectionType: 'FirewallPolicyFilterRuleCollection'
        priority: 400
        action: {
          type: 'Allow'
        }
        rules: [
          {
            ruleType: 'ApplicationRule'
            description: 'Allow web out'
            name: 'AllowWebOut'
            sourceAddresses: ['*']
            protocols: [
              { port: 443, protocolType: 'Https' }
              { port: 80, protocolType: 'Http' }
            ]
            targetFqdns: [
              '*' // this pattern is commonly used for “all FQDNs” in app rules
            ]
          }
        ]
      }
    ]
  }
}

output publicIpV4 string = firewallPip.properties.ipAddress
output firewallPrivateIp string = firewall.properties.ipConfigurations[0].properties.privateIPAddress
