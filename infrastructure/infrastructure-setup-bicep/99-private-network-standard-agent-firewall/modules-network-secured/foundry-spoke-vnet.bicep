@description('Azure region for the deployment')
param location string

@description('The name of the Foundry spoke virtual network')
param vnetName string = 'foundry-spoke-vnet'

@description('Address space for the Foundry Spoke VNet')
param vnetAddressPrefix string = '10.2.0.0/16'

@description('The name of the Agents Subnet')
param agentSubnetName string = 'agent-subnet'

@description('The name of the Private Endpoint subnet')
param peSubnetName string = 'pe-subnet'

@description('Next hop IP address for the firewall (for UDR)')
param firewallPrivateIp string

@description('Custom DNS server IP (DNS Resolver inbound endpoint)')
param dnsServerIp string

var agentSubnet = cidrSubnet(vnetAddressPrefix, 24, 0)
var peSubnet = cidrSubnet(vnetAddressPrefix, 24, 1)
var vmSubnet = cidrSubnet(vnetAddressPrefix, 24, 2)

resource routeTable 'Microsoft.Network/routeTables@2022-11-01' = {
  name: '${vnetName}-rt'
  location: location
  properties: {
    routes: [
      {
        name: 'InternetViaFirewall'
        properties: {
          nextHopType: 'VirtualAppliance'
          addressPrefix: '0.0.0.0/0'
          nextHopIpAddress: firewallPrivateIp
        }
      }
    ]
  }
}

resource networkSecurityGroup 'Microsoft.Network/networkSecurityGroups@2022-05-01' = {
  name: '${vnetName}-vm-nsg'
  location: location
  properties: {
    securityRules: [
      {
        name: 'default-allow-3389-from-bastion'
        properties: {
          priority: 999
          access: 'Allow'
          direction: 'Inbound'
          destinationPortRange: '3389'
          protocol: 'Tcp'
          sourceAddressPrefix: '168.63.129.16/32'
          destinationAddressPrefix: '*'
          sourcePortRange: '*'
        }
      }
    ]
  }
}

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressPrefix
      ]
    }
    dhcpOptions: {
      dnsServers: [
        dnsServerIp
      ]
    }
    subnets: [
      {
        name: agentSubnetName
        properties: {
          addressPrefix: agentSubnet
          delegations: [
            {
              name: 'Microsoft.app/environments'
              properties: {
                serviceName: 'Microsoft.App/environments'
              }
            }
          ]
          routeTable: {
            id: routeTable.id
          }
        }
      }
      {
        name: peSubnetName
        properties: {
          addressPrefix: peSubnet
        }
      }
      {
        name: 'VirtualMachines'
        properties: {
          addressPrefix: vmSubnet
          routeTable: {
            id: routeTable.id
          }
          networkSecurityGroup: {
            id: networkSecurityGroup.id
          }
        }
      }
    ]
  }
}

output virtualNetworkName string = virtualNetwork.name
output virtualNetworkId string = virtualNetwork.id
output agentSubnetId string = '${virtualNetwork.id}/subnets/${agentSubnetName}'
output peSubnetId string = '${virtualNetwork.id}/subnets/${peSubnetName}'
output vmSubnetName string = 'VirtualMachines'
output agentSubnetName string = agentSubnetName
output peSubnetName string = peSubnetName
output routeTableName string = routeTable.name
