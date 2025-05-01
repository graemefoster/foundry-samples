# Sample of Azure.AI.Agents with local function calling

In this example we are demonstrating how to use the local functions with the agents. The functions can be used to provide agent specific information in response to user question.

1. First get `ProjectEndpoint` and `ModelDeploymentName` from config and create a `PersistentAgentsClient`.
```C# Snippet:AgentsFunctions_CreateClient
var projectEndpoint = configuration["ProjectEndpoint"]);
var modelDeploymentName = configuration["ModelDeploymentName"];
PersistentAgentsClient client = new(new Uri(projectEndpoint) new DefaultAzureCredential());
```

2 Define three simple local functions: `GetUserFavoriteCity` that always returns "Seattle, WA" and `GetCityNickname`, which will handle only "Seattle, WA" and will throw exception in response to other city names. The last function `GetWeatherAtLocation` returns weather at Seattle, WA. For each function we need to create `FunctionToolDefinition`, which defines function name, description and parameters. The `FunctionToolDefinition` enables help the agent use the local functions.
```C# Snippet:AgentsFunctionsDefineFunctionTools
// Example of a local function that requires no parameters and returns a string.
string GetUserFavoriteCity() => "Seattle, WA";
// Example tool definition that will be shared with agent.
FunctionToolDefinition getUserFavoriteCityTool = new("getUserFavoriteCity", "Gets the user's favorite city.");
// Example local function that has a single required paramter, location.
string GetCityNickname(string location) => location switch
{
    "Seattle, WA" => "The Emerald City",
    _ => throw new NotImplementedException(),
};
// Example tool definition that will be shared with agent which defines a required paramter named location.
FunctionToolDefinition getCityNicknameTool = new(
    name: "getCityNickname",
    description: "Gets the nickname of a city, e.g. 'LA' for 'Los Angeles, CA'.",
    parameters: BinaryData.FromObjectAsJson(
        new
        {
            Type = "object",
            Properties = new
            {
                Location = new
                {
                    Type = "string",
                    Description = "The city and state, e.g. San Francisco, CA",
                },
            },
            Required = new[] { "location" },
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));
// Example local function with one required and one optional parameter
string GetWeatherAtLocation(string location, string temperatureUnit = "f") => location switch
{
    "Seattle, WA" => temperatureUnit == "f" ? "70f" : "21c",
    _ => throw new NotImplementedException()
};
// Example tool definition that will be shared with agent which defines a required paramter named location and optional paramter named unit.
FunctionToolDefinition getCurrentWeatherAtLocationTool = new(
    name: "getCurrentWeatherAtLocation",
    description: "Gets the current weather at a provided location.",
    parameters: BinaryData.FromObjectAsJson(
        new
        {
            Type = "object",
            Properties = new
            {
                Location = new
                {
                    Type = "string",
                    Description = "The city and state, e.g. San Francisco, CA",
                },
                Unit = new
                {
                    Type = "string",
                    Enum = new[] { "c", "f" },
                },
            },
            Required = new[] { "location" },
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }));
```

3. Create a function named `GetResolvedToolOutput` to faciliate an agent's request for data from a local function. This function attempts to find, and run the local function and supply necessary paramters. The results of the function are wrapped in a `ToolOutput`. object.
```C# Snippet:AgentsFunctionsHandleFunctionCalls
ToolOutput GetResolvedToolOutput(RequiredToolCall toolCall)
{
    if (toolCall is RequiredFunctionToolCall functionToolCall)
    {
        if (functionToolCall.Name == getUserFavoriteCityTool.Name)
        {
            return new ToolOutput(toolCall, GetUserFavoriteCity());
        }
        using JsonDocument argumentsJson = JsonDocument.Parse(functionToolCall.Arguments);
        if (functionToolCall.Name == getCityNicknameTool.Name)
        {
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            return new ToolOutput(toolCall, GetCityNickname(locationArgument));
        }
        if (functionToolCall.Name == getCurrentWeatherAtLocationTool.Name)
        {
            string locationArgument = argumentsJson.RootElement.GetProperty("location").GetString();
            if (argumentsJson.RootElement.TryGetProperty("unit", out JsonElement unitElement))
            {
                string unitArgument = unitElement.GetString();
                return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument, unitArgument));
            }
            return new ToolOutput(toolCall, GetWeatherAtLocation(locationArgument));
        }
    }
    return null;
}
```

4. Create an agent with the `FunctionToolDefinitions` from step 2.

Synchronous sample:
```C# Snippet:AgentsFunctionsSyncCreateAgentWithFunctionTools
// note: parallel function calling is only supported with newer models like gpt-4-1106-preview
PersistentAgent agent = client.CreateAgent(
    model: modelDeploymentName,
    name: "SDK Test Agent - Functions",
        instructions: "You are a weather bot. Use the provided functions to help answer questions. "
            + "Customize your responses to the user's preferences as much as possible and use friendly "
            + "nicknames for cities whenever possible.",
    tools: [getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool]
    );
```

Asynchronous sample:
```C# Snippet:AgentsFunctionsCreateAgentWithFunctionTools
// note: parallel function calling is only supported with newer models like gpt-4-1106-preview
PersistentAgent agent = await client.CreateAgentAsync(
    model: modelDeploymentName,
    name: "SDK Test Agent - Functions",
        instructions: "You are a weather bot. Use the provided functions to help answer questions. "
            + "Customize your responses to the user's preferences as much as possible and use friendly "
            + "nicknames for cities whenever possible.",
    tools: [getUserFavoriteCityTool, getCityNicknameTool, getCurrentWeatherAtLocationTool ]
    );
```

5. This step has three parts that will start the process to answer a user's question.

* First create a `PersistentAgentThread` establishing a session with an agent.
* Then add a `ThreadMessage` which is a question for the agent to answer using `CreateMessage` from `PersistentAgentsClient`
* Next, create a `ThreadRun` which starts the answering of a user's question by the agent.

Synchronous sample:
```C# Snippet:AgentsFunctionsSync_CreateRun
PersistentAgentThread thread = client.CreateThread();

client.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");

ThreadRun run = client.CreateRun(thread, agent);
```

Asynchronous sample:
```C# Snippet:AgentsFunctions_CreateRun
PersistentAgentThread thread = await client.CreateThreadAsync();

await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "What's the weather like in my favorite city?");

ThreadRun run = await client.CreateRunAsync(thread, agent);
```

6. Next, monitor `ThreadRun` by polling and examining the `ThreadRun.Status`. When `ThreadRun.Status` is `RunStatus.RequiresAction` pass each `RequiredToolCall` from the agent to `GetResolvedToolOutput` in order to run the local functions.

Synchronous sample:
```C# Snippet:AgentsFunctionsSyncHandlePollingWithRequiredAction
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.GetRun(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction
        && run.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        List<ToolOutput> toolOutputs = [];
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            toolOutputs.Add(GetResolvedToolOutput(toolCall));
        }
        run = client.SubmitToolOutputsToRun(run, toolOutputs);
    }
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

Asynchronous sample:
```C# Snippet:AgentsFunctionsHandlePollingWithRequiredAction
do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    run = await client.GetRunAsync(thread.Id, run.Id);

    if (run.Status == RunStatus.RequiresAction
        && run.RequiredAction is SubmitToolOutputsAction submitToolOutputsAction)
    {
        List<ToolOutput> toolOutputs = [];
        foreach (RequiredToolCall toolCall in submitToolOutputsAction.ToolCalls)
        {
            toolOutputs.Add(GetResolvedToolOutput(toolCall));
        }
        run = await client.SubmitToolOutputsToRunAsync(run, toolOutputs);
    }
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

7. Now, that the `ThreadRun` has completed it is time to display the messages in chronological order. Using the `PersistentAgentsClient.GetMessages` to get `PageableList<ThreadMessage>` which contain the user's question and the answer by the agent.

Sample output by agent:
    user: What's the weather like in my favorite city?
    assistant: The weather in "The Emerald City" is currently a pleasant 70°F. Perfect for a stroll around town!

Synchronous sample:
```C# Snippet:AgentsFunctionsSync_ListMessages
PageableList<ThreadMessage> messages = client.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            Console.Write($"{threadMessage.Role}: {textItem.Text}");
        }
        Console.WriteLine();
    }
}
```

Asynchronous sample:
```C# Snippet:AgentsFunctions_ListMessages
PageableList<ThreadMessage> messages = await client.GetMessagesAsync(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            Console.Write($"{threadMessage.Role}: {textItem.Text}");
        }
        Console.WriteLine();
    }
}
```

8. Finally, delete the resources created in this sample.

Synchronous sample:
```C# Snippet:AgentsFunctionsSync_Cleanup
client.DeleteThread(thread.Id);
client.DeleteAgent(agent.Id);
```

Asynchronous sample:
```C# Snippet:AgentsFunctions_Cleanup
await client.DeleteThreadAsync(thread.Id);
await client.DeleteAgentAsync(agent.Id);
```
