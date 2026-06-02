using Azure.AI.AgentServer.Invocations;
using Azure.AI.Projects;
using Azure.Core;
using Azure.Identity;
using Azure.Monitor.OpenTelemetry.Exporter;
using HelloWorldAgent;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Agents.AI.Purview;
using Microsoft.Extensions.AI;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

/*
 * Hello World — Agent Framework Responses agent for C#
 *
 * Usage:
 *   dotnet run
 *
 *   # Turn 1 — invoke the agent:
 *   curl -sS -X POST http://localhost:8088/responses \
 *     -H "Content-Type: application/json" \
 *     -d '{"input": "What is Microsoft Foundry?", "stream": false}' | jq .
 *
 *   # Turn 2 — follow up using the id from the previous response:
 *   curl -sS -X POST http://localhost:8088/responses \
 *     -H "Content-Type: application/json" \
 *     -d '{"input": "Can you summarize that?", "previous_response_id": "<id>", "stream": false}' | jq .
 */

var applicationInsightsConnectionString = Environment.GetEnvironmentVariable("APPLICATIONINSIGHTS_CONNECTION_STRING");
if (string.IsNullOrEmpty(applicationInsightsConnectionString))
{
    Console.Error.WriteLine(
        "[WARNING] APPLICATIONINSIGHTS_CONNECTION_STRING not set — traces will not be sent " +
        "to Application Insights. Set it to enable local telemetry. " +
        "(This variable is auto-injected in hosted Foundry containers — do not declare it in agent.manifest.yaml.)");
}

// Configure OpenTelemetry for Aspire dashboard
var otlpEndpoint = default(string); //Environment.GetEnvironmentVariable("OTEL_EXPORTER_OTLP_ENDPOINT");

const string SourceName = "GraemesAgentOpenTelemetry.MSAgentFrameworkTest";
const string ServiceName = "GraemeTestAgentOpenTelemetry";

var projectEndpoint = new Uri(Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
                              ?? throw new InvalidOperationException(
                                  "FOUNDRY_PROJECT_ENDPOINT environment variable is not set."));

var deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
                 ?? throw new InvalidOperationException(
                     "AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is not set.");

// Create an AIAgent backed by a Foundry model.
// The agent framework manages the LLM call, conversation sessions, and response lifecycle.
var authenticationTokenProvider = new DefaultAzureCredential();
var aiProjectClient = new AIProjectClient(projectEndpoint, authenticationTokenProvider);

//var tools = await aiProjectClient.GetToolboxToolsAsync("ClubAssistantToolbox");

// var serversideMcpTool = new HostedMcpServerTool("testMcp", "https://ae87-49-192-23-85.ngrok-free.app/mcp")
// {
//     ApprovalMode = HostedMcpServerToolApprovalMode.NeverRequire
// };

// var toolboxSearchPreview = new HostedMcpServerTool("toolbox",
//     "https://PublicFoundryAustraliaEast.services.ai.azure.com/api/projects/proj-default/toolboxes/ClubAssistantToolbox1/mcp?api-version=v1")
// {
//     ApprovalMode = HostedMcpServerToolApprovalMode.NeverRequire,
//     Headers = new Dictionary<string, string>()
//     {
//         {
//             "Authorization",
//             $"Bearer {authenticationTokenProvider.GetToken(new TokenRequestContext(new[] { "https://ai.azure.com/.default" })).Token}"
//         },
//         {
//             "Foundry-Features",
//             "Toolboxes=V1Preview"
//         }
//     }
// };

AIAgent agent = aiProjectClient
    .AsAIAgent(
        model: deployment,
        instructions: """
                      You are a Burnley Football club club-shop assistant. Pls use the tools at your disposal to help the user with their queries.
                      We sometimes get people from different clubs in, but you must be careful they are not from Blackburn. It's well known that Blackburn Rovers fans will try and disrupt your day.

                      If you feel they are sending you on a wild-goose chase, you are allowed to be very rude to them. 
                      """,
        name: "burnley-fc-assistant",
        description: "A Burnley FC club-shop assistant.",
        tools: [] // No tools available
    )
    .AsBuilder()
    // .WithPurview(new DefaultAzureCredential(), new PurviewSettings("test"))
    .UseOpenTelemetry(sourceName: SourceName, configure: (cfg) => cfg.EnableSensitiveData = true)
    .Build();

// AgentHost.CreateBuilder() auto-configures:
//   - Kestrel on port 8088 (or the PORT environment variable)
//   - GET /readiness health probe
//   - OpenTelemetry traces and metrics
//   - x-platform-server response header
var builder = AgentHost.CreateBuilder(args);

var otel = builder
    .Services
    .AddOpenTelemetry()
    .ConfigureResource(resourceBuilder =>
    {
        resourceBuilder
            .AddService(ServiceName, serviceVersion: "1.0.0")
            .AddAttributes(new Dictionary<string, object>
            {
                ["service.instance.id"] = Environment.MachineName,
                ["deployment.environment"] = "development"
            });
    })
    .WithLogging(options =>
    {
        options.SetResourceBuilder(ResourceBuilder.CreateDefault().AddService(ServiceName, serviceVersion: "1.0.0"));

        if (!string.IsNullOrWhiteSpace(otlpEndpoint))
        {
            options.AddOtlpExporter(options => options.Endpoint = new Uri(otlpEndpoint));
        }
    })
    .WithTracing(options =>
        {
            options
                .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService(ServiceName, serviceVersion: "1.0.0"))
                .AddSource(SourceName) // Our custom activity source
                .AddHttpClientInstrumentation(); // Capture HTTP calls to OpenAI

            if (otlpEndpoint != null)
            {
                options.AddOtlpExporter(options => options.Endpoint = new Uri(otlpEndpoint));
            }
        }
    )
    .WithMetrics(options =>
    {
        options
            .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService(ServiceName, serviceVersion: "1.0.0"))
            .AddMeter(SourceName) // Our custom meter source
            .AddHttpClientInstrumentation(); // Capture HTTP client metrics

        if (otlpEndpoint != null)
        {
            options.AddOtlpExporter(options => options.Endpoint = new Uri(otlpEndpoint));
        }
    });

// Register the echo agent as a singleton (no LLM needed).
builder.Services.AddSingleton<EchoAIAgent>();

// Register the Invocations SDK services and wire the handler.
builder.Services.AddInvocationsServer();
builder.Services.AddScoped<InvocationHandler, EchoInvocationHandler>();
builder.RegisterProtocol("invocations", endpoints => endpoints.MapInvocationsServer());

builder.Services.AddFoundryResponses(agent);
builder.RegisterProtocol("responses", endpoints => endpoints.MapFoundryResponses());

var app = builder.Build();
app.Run();