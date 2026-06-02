param(
    [Parameter(Mandatory = $false)]
    [string]$Endpoint = "https://grfpublicfoundryaueast.services.ai.azure.com/api/projects/proj-default",

    [Parameter(Mandatory = $false)]
    [string]$ModelDeployment = "gpt-4o",

    [string]$AgentName = "azure-function-agent",
    [string]$Description = "Sample agent created via REST",
    [string]$Instructions = "You are a weather assistant. Use your tools to get the current weather information and provide it to the user.",
    [string]$Prompt = "What's the weather in Perth, Australia today?",
    [string]$ApiVersion = "2025-11-15-preview"
)

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    throw "Azure CLI (az) is required."
}

$tokenJson = az account get-access-token --resource https://ai.azure.com/ 2>$null | ConvertFrom-Json
if (-not $tokenJson.accessToken) {
    throw "Failed to acquire Azure AI Foundry access token. Please run az login"
}

$headers = @{
    Authorization  = "Bearer $($tokenJson.accessToken)"
    "Content-Type" = "application/json"
}

$ErrorActionPreference = "Stop"


function Invoke-FoundryRequest {
    param(
        [string]$Method,
        [string]$Uri,
        [hashtable]$Headers,
        [string]$Body
    )

    Write-Host ""
    Write-Host "[$Method] $Uri"
    if ($Body) {
        Write-Host "Request Body:`n$Body"
    }

    $invokeParams = @{
        Method             = $Method
        Uri                = $Uri
        Headers            = $Headers
        ErrorAction        = "Stop"
        StatusCodeVariable = "sc"
    }
    if ($Body) {
        $invokeParams["Body"] = $Body
    }

    try {
        $result = Invoke-RestMethod @invokeParams
        Write-Host "Status: $sc"
        return $result
    }
    catch {
        $resp = $_.Exception.Response
        if ($resp) {
            $statusName = $resp.StatusCode
            $statusValue = [int]$resp.StatusCode
            Write-Host "Status: $statusName [$statusValue]"
            try {
                $stream = $resp.GetResponseStream()
                if ($stream) {
                    $reader = New-Object System.IO.StreamReader($stream)
                    $responseText = $reader.ReadToEnd()
                    if ($responseText) {
                        Write-Host "Error Body:`n$responseText"
                    }
                    $reader.Dispose()
                    $stream.Dispose()
                }
            }
            catch {}
        }
        throw
    }
}

$trimmedEndpoint = $Endpoint.TrimEnd('/')
$createAgentUri = "${trimmedEndpoint}/agents?api-version=${ApiVersion}"
$agentUri = "${trimmedEndpoint}/agents/${AgentName}?api-version=${ApiVersion}"
$createResponseUri = "${trimmedEndpoint}/openai/responses?api-version=${ApiVersion}"

$createBody = @{
    name        = $AgentName
    description = $Description
    definition  = @{
        kind         = "prompt"
        model        = $ModelDeployment
        instructions = $Instructions
        temperature  = 0.3
        tools        = @(
            @{
                name           = "GetWeatherInfo"
                type           = "azure_function"
                azure_function = @{
                    function       = @{
                        name       = "GetWeatherInfo"
                        description    = "Azure Function tool for getting weather information"
                        parameters = @{
                            type       = "object"
                            properties = @{
                                location = @{
                                    type        = "string"
                                    description = "The location to get the weather for"
                                }
                                outputqueueuri = @{
                                    type        = "string"
                                    description = "The full output queue uri."
                                }
                            }
                        }
                    }
                    input_binding  = @{
                        type          = "storage_queue"
                        storage_queue = @{
                            queue_name             = "inputqueuetest"
                            queue_service_endpoint = "https://grfteststoragefunctionag.queue.core.windows.net/"
                        }
                    }
                    output_binding = @{
                        type          = "storage_queue"
                        storage_queue = @{
                            queue_name             = "outputqueuetest"
                            queue_service_endpoint = "https://grfteststoragefunctionag.queue.core.windows.net/"
                        }
                    }
                }
            }
        )
    }
} | ConvertTo-Json -Depth 6

$agentVersion = $null
try {
    Write-Host "Creating agent '${AgentName}'..."
    $agent = Invoke-FoundryRequest -Method Post -Uri $createAgentUri -Headers $headers -Body $createBody
    if (-not $agent) {
        throw "Agent creation response missing body."
    }

    $agentVersion = $agent.versions.latest.version
    if (-not $agentVersion) {
        throw "Agent creation response missing version."
    }

    Write-Host "Agent created (version: ${agentVersion})."

    $responseBody = @{
        agent = @{
            type    = "agent_reference"
            name    = $AgentName
            version = $agentVersion
        }
        input = @(
            @{
                role    = "user"
                content = @(
                    @{
                        type = "input_text"
                        text = $Prompt
                    }
                )
            }
        )
    } | ConvertTo-Json -Depth 8

    Write-Host "Requesting response from '${AgentName}'..."
    $responseData = Invoke-FoundryRequest -Method Post -Uri $createResponseUri -Headers $headers -Body $responseBody

    Write-Host $responseData.output[0].content[0].text

    Write-Host "Agent response:`n${assistantText}"
}
finally {
    Write-Host "Cleaning up agent '${AgentName}'..."
    try {
        $deleteUri = $agentUri
        if ($agentVersion) {
            $deleteUri = "${trimmedEndpoint}/agents/${AgentName}?api-version=${ApiVersion}&version=${agentVersion}"
        }
        Invoke-FoundryRequest -Method Delete -Uri $deleteUri -Headers $headers | Out-Null
        Write-Host "Agent deleted."
    }
    catch {
        Write-Warning "Failed to delete agent '${AgentName}': $($_.Exception.Message)"
    }
}
