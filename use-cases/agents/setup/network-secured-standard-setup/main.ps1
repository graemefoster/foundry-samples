# Define the base directory relative to the script location
$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Update paths to use relative references
$bicepAccountCreate = Join-Path $baseDir "main-accountcreate.bicep"
$checkCapabilityScript = Join-Path $baseDir "checkcapabilityhostreadiness.ps1"
$bicepProjectCreate = Join-Path $baseDir "main-projectcreate.bicep"

# Run the main-accountcreate.bicep file
Write-Host "Running $bicepAccountCreate..."
az deployment sub create --template-file $bicepAccountCreate
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run $bicepAccountCreate. Exiting script."
    exit $LASTEXITCODE
}
# Retrieve outputs from the main-accountcreate.bicep deployment
Write-Host "Retrieving outputs from $bicepAccountCreate deployment..."
$accountCreateOutputs = az deployment sub show --name main-accountcreate --query properties.outputs -o json | ConvertFrom-Json

if (-not $accountCreateOutputs) {
    Write-Error "Failed to retrieve outputs from $bicepAccountCreate. Exiting script."
    exit 1
}

# Extract the three output variables
$output1 = $accountCreateOutputs.output1.value
$output2 = $accountCreateOutputs.output2.value
$output3 = $accountCreateOutputs.output3.value

# Pass the outputs as arguments to the checkcapabilityhostreadiness.ps1 script
Write-Host "Passing outputs to $checkCapabilityScript..."
& $checkCapabilityScript -Output1 $output1 -Output2 $output2 -Output3 $output3
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run $checkCapabilityScript with provided outputs. Exiting script."
    exit $LASTEXITCODE
}
# Run the checkcapabilityhostreadiness.ps1 script
Write-Host "Running $checkCapabilityScript..."
& $checkCapabilityScript
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run $checkCapabilityScript. Exiting script."
    exit $LASTEXITCODE
}

# Run the main-projectcreate.bicep file
Write-Host "Running $bicepProjectCreate..."
az deployment sub create --template-file $bicepProjectCreate
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run $bicepProjectCreate. Exiting script."
    exit $LASTEXITCODE
}

Write-Host "All tasks completed successfully."