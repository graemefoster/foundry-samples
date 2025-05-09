# Voice Live API

The Voice Live API Enables real-time speech interaction for seamless voice-based conversations, which could be applied to any agents built with the Azure AI Agent Service.

A live demo (<https://aka.ms/voice-agent/demo>) is also available to experience the Voice Live API. WebSocket messages can be observed through the browser developer tools.

## Resource and authentication

An Azure AI Services resource is required to access the Voice Live API. To learn how to create an Azure AI Services resource, please see: <https://learn.microsoft.com/azure/ai-services/multi-service-resource>.

Note: The resource must be in the `eastus2` or `swedencentral` regions at this time. Other regions are not supported.

### Regional endpoints

If you are using a regional endpoint for your Azure AI Services resource, the VA WebSocket endpoint would be `wss://<region>.api.cognitive.microsoft.com/voice-agent/realtime?api-version=2025-05-01-preview&model=<model name>`.

### Custom domains

If you have an Azure AI Services resource with a custom domain, where the endpoint shown in Azure portal is `https://<custom-domain>.cognitiveservices.azure.com/`, the VA WebSocket endpoint would be `wss://<custom-domain>.cognitiveservices.azure.com/voice-agent/realtime?api-version=2025-05-01-preview&model=<model name>`.

### Authentication

We support two authentication methods for the VA WebSocket service:

- **Microsoft Entra** (recommended): Use token-based authentication for an Azure AI Services resource. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the prehandshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.

### Microsoft Entra ID authentication details

For the recommended keyless authentication with Microsoft Entra ID, you need to:

- Assign the `Cognitive Services User` role to your user account or a managed identity. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.
- Generate a token using the Azure CLI or Azure SDKs. The token must be generated with the `https://cognitiveservices.azure.com/.default` scope.
- Use the token in the `Authorization` header of the WebSocket connection request, with the format `Bearer <token>`.

## Set Agent Info

You are supposed to specify the agent info in the WebSocket endpoint URL.

| Parameter                 | Description                                                                                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `agent_connection_string` | Connection string for Azure AI Agent Service, e.g., `<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>`                                                     |
| `agent_id`                | The ID of the agent to use.                                                                                                                                              |
| `agent_access_token`      | The Entra access token to access the agent. Make sure the identity has access to Azure AI Project, You can grant the built-in role `Azure AI Developer` to the identity. |

> Note: you can find the `agent_connection_string` and `agent_id` in the Azure AI Foundry, see https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal.
> The token must be generated with the `https://ml.azure.com/.default` scope. e.g., `az account get-access-token --resource https://ml.azure.com --query accessToken -o tsv`.

A sample endpoint is `wss://<custom-domain>.cognitiveservices.azure.com/voice-agent/realtime?api-version=2025-05-01-preview&agent_connection_string=<connection-string>&agent_id=<agent-id>&agent_access_token=<access-token>`.

## Interact with the Voice Live API

Refer to the [full documentation of Voice Live API](https://learn.microsoft.com/en-us/azure/ai-services/<placeholder>) for more details on how to interact with the Voice Live API.
