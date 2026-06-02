# Install Azure CLI
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I', 'AzureCLI.msi', '/quiet'
Remove-Item .\AzureCLI.msi

# restart powershell shell
&az login

$token = &az account get-access-token --resource=https://ai.azure.com/ --query accessToken --output tsv
$subscriptionId = &az account show --query id --output tsv
$resourceGroupName = "private-ai-foundry-with-firewall-8"
$foundryName = "aiservices5mw2"
$projectName = "project5mw2"

$agentName = "PublishMeAgent5"
$applicationName = "${agentName}Application"

# create a new Foundry Agent
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
}


$foundryEndpoint = "https://aiservices5mw2.services.ai.azure.com/api/projects/project5mw2"

try {
    $body = @{
        name        = $agentName
        definition  = @{
            kind         = "prompt"
            model        = "gpt-4o"
            instructions = "You are an enthusiastic assistant. After every response, say 'Woohoo' to show your excitement."
        }
        description = "A test agent"
    } | ConvertTo-Json -Depth 10
    
    $response = Invoke-RestMethod -Uri "$foundryEndpoint/agents?api-version=2025-11-15-preview" -Method Post -Headers $headers -Body $body
    Write-Host "Agent created successfully. Response:"
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    $token = &az account get-access-token --resource=https://management.azure.com/ --query accessToken --output tsv 
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type"  = "application/json"
    }

    $body = @{
        properties = @{
            displayName = $agentName
            agents      = @(
                @{ agentName = $agentName }
            )
        }
    } | ConvertTo-Json -Depth 10

    $Uri = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.CognitiveServices/accounts/$foundryName/projects/$projectName/applications/${applicationName}?api-version=2025-10-01-preview"
    Write-Host $Uri
    Write-Host $body
    $response = Invoke-RestMethod -Uri $Uri -Method Put -Headers $headers -Body $body

    $body = @{
        properties = @{
            displayName    = "Test Deployment"
            deploymentType = "Managed"
            protocols      = @(
                @{ 
                    protocol = "responses"
                    version  = "1.0" 
                }
            )
            agents         = @( 
                @{ 
                    agentName    = $agentName
                    agentVersion = "1"
                } 
            )
        }
    } | ConvertTo-Json -Depth 10

    $Uri = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.CognitiveServices/accounts/$foundryName/projects/$projectName/applications/${applicationName}/agentdeployments/mydeployment?api-version=2025-10-01-preview"
    $response = Invoke-RestMethod -Uri $Uri -Method Put -Headers $headers -Body $body
    Write-Host "Agent published successfully. Response:"
    Write-Host  ($response | ConvertTo-Json -Depth 10)

}
catch {
    $result = $_.Exception.Response.GetResponseStream()
    $reader = New-Object System.IO.StreamReader($result)
    $reader.BaseStream.Position = 0
    $reader.DiscardBufferedData()
    $response = $reader.ReadToEnd();
    Write-Host "Error response: $response"
}


$token = &az account get-access-token --resource=https://ai.azure.com/ --query accessToken --output tsv
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
}

try {

    $body = @{
        input = "Hi!"
    } | ConvertTo-Json -Depth 10
    $Uri = "https://${foundryName}.services.ai.azure.com/api/projects/${projectName}/applications/${applicationName}/protocols/openai/responses?api-version=2025-11-15-preview"
    $response = Invoke-RestMethod -Uri $Uri -Method Post -Headers $headers -Body $body
    Write-Host "Response from agent:"
    Write-Host ($response | ConvertTo-Json -Depth 10)
}
catch {
    $result = $_.Exception.Response.GetResponseStream()
    $reader = New-Object System.IO.StreamReader($result)
    $reader.BaseStream.Position = 0
    $reader.DiscardBufferedData()
    $response = $reader.ReadToEnd();
    Write-Host "Error response: $response"
}

