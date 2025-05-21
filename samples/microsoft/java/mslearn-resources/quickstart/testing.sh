#!/bin/bash
# Automated testing script for Azure AI Foundry Java Samples
# Usage: ./testing.sh [SampleName]

set -e  # Exit on error

# Function to display colored output
print_color() {
    color_code=$1
    shift
    echo -e "\033[${color_code}m$@\033[0m"
}

# Function to validate environment variables
validate_env() {
    missing_vars=()
    
    if [ -z "$AZURE_ENDPOINT" ]; then missing_vars+=("AZURE_ENDPOINT"); fi
    if [ -z "$AZURE_DEPLOYMENT" ]; then missing_vars+=("AZURE_DEPLOYMENT"); fi
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        print_color "31" "ERROR: Missing required environment variables:"
        for var in "${missing_vars[@]}"; do
            print_color "31" "  - $var"
        done
        print_color "31" "Please create a .env file with these variables or set them in your environment."
        exit 1
    fi
}

# Function to run a test and track its result
run_test() {
    sample=$1
    print_color "36" "\n=============================================================="
    print_color "36" "   RUNNING TEST: $sample"
    print_color "36" "==============================================================\n"
    
    # Run the test
    if mvn compile exec:java -Dexec.mainClass="com.azure.ai.foundry.samples.$sample"; then
        print_color "32" "\n✓ TEST PASSED: $sample"
        return 0
    else
        print_color "31" "\n✗ TEST FAILED: $sample"
        return 1
    fi
}

# Check for Java and Maven
if ! command -v java &> /dev/null; then
    print_color "31" "Error: Java is not installed or not in PATH"
    exit 1
fi

if ! command -v mvn &> /dev/null; then
    print_color "31" "Error: Maven is not installed or not in PATH"
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    print_color "33" "Warning: .env file not found. Creating from template..."
    if [ -f .env.template ]; then
        cp .env.template .env
        print_color "33" "Created .env file from template. Please edit it with your actual configuration values before running tests."
        exit 1
    else
        print_color "31" "Error: .env.template file not found. Cannot create .env file."
        exit 1
    fi
fi

# Check if user is logged in with Azure CLI
print_color "36" "Checking Azure CLI login status..."
if ! az account show > /dev/null 2>&1; then
    print_color "31" "Error: You are not logged in with the Azure CLI. Please run 'az login' first."
    exit 1
else
    print_color "32" "Azure CLI login validated."
fi

# Check for required environment variables
print_color "36" "Validating environment variables..."
missing_vars=""

while IFS='=' read -r key value || [ -n "$key" ]; do
    # Ignore comment lines and empty lines
    [[ $key == \#* ]] && continue
    [[ -z "$key" ]] && continue
    
    key=$(echo $key | xargs)  # Trim whitespace

    if [[ "$key" == "AZURE_ENDPOINT" && "$value" == *"your_endpoint_here"* ]]; then
        missing_vars="$missing_vars AZURE_ENDPOINT"
    fi

    if [[ "$key" == "AZURE_DEPLOYMENT" && "$value" == *"your_deployment_name_here"* ]]; then
        missing_vars="$missing_vars AZURE_DEPLOYMENT"
    fi
done < .env

if [ ! -z "$missing_vars" ]; then
    print_color "31" "Error: The following environment variables need to be updated in .env file:$missing_vars"
    print_color "31" "Please edit the .env file with your actual configuration values before running tests."
    exit 1
else
    print_color "32" "Environment variables validation passed."
fi

# Build the project first
print_color "36" "\n=============================================================="
print_color "36" "   BUILDING PROJECT"
print_color "36" "==============================================================\n"

if ! mvn clean compile; then
    print_color "31" "Error: Failed to build the project"
    exit 1
fi

# Track overall success
success=true

# If a specific test is specified, run only that test
if [ "$1" != "" ]; then
    if run_test "$1"; then
        print_color "32" "\nSingle test completed successfully."
    else
        print_color "31" "\nSingle test failed."
        exit 1
    fi
    exit 0
fi

# Run all tests in sequence
samples=(
    "CreateProject"
    "ChatCompletionSample"
    "ChatCompletionStreamingSample"
    "AgentSample"
    "FileSearchAgentSample"
    "EvaluateAgentSample"
)

# Arrays to track results
passed_tests=()
failed_tests=()

# Run each test
for sample in "${samples[@]}"; do
    if run_test "$sample"; then
        passed_tests+=("$sample")
    else
        failed_tests+=("$sample")
        success=false
    fi
    
    # Short pause between tests
    sleep 2
done

# Print summary
print_color "36" "\n=============================================================="
print_color "36" "   TEST SUMMARY"
print_color "36" "==============================================================\n"

print_color "32" "PASSED TESTS (${#passed_tests[@]}):"
for test in "${passed_tests[@]}"; do
    print_color "32" "  ✓ $test"
done

if [ ${#failed_tests[@]} -gt 0 ]; then
    print_color "31" "\nFAILED TESTS (${#failed_tests[@]}):"
    for test in "${failed_tests[@]}"; do
        print_color "31" "  ✗ $test"
    done
    print_color "31" "\nSome tests failed. Please check the logs above for details."
    exit 1
else
    print_color "32" "\nAll tests passed successfully!"
fi
