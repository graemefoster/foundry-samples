# Sample for using additional messages while creating agent run in Azure.AI.Agents

1. First get `ProjectEndpoint` and `ModelDeploymentName` from config and create a `PersistentAgentsClient`.

```C# Snippet:Sample_Agent_Multiple_Messages_Create
var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
PersistentAgentsClient client = new(new Uri(projectEndpoint), new DefaultAzureCredential());
```

2. Next we will need to create an agent.

Synchronous sample:
```C# Snippet:Sample_Agent_Multiple_Messages_Create
PersistentAgent agent = client.CreateAgent(
    model: modelDeploymentName,
    name: "Math Tutor",
    instructions: "You are a personal electronics tutor. Write and run code to answer questions.",
    tools: [new CodeInterpreterToolDefinition()]);
```

Asynchronous sample:
```C# Snippet:Sample_Agent_Multiple_Messages_CreateAsync
PersistentAgent agent = await client.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Math Tutor",
    instructions: "You are a personal electronics tutor. Write and run code to answer questions.",
    tools: [new CodeInterpreterToolDefinition()]);
```

3. Create the thread and run. In this example we are adding two extra messages to the thread, one with `Agent` and another with `User` role.

Synchronous sample:
```C# Snippet:Sample_Agent_Multiple_Messages_Run
PersistentAgentThread thread = client.CreateThread();
client.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the impedance formula?");

ThreadRun agentRun = client.CreateRun(
    threadId: thread.Id,
    agent.Id,
    additionalMessages: [
        new ThreadMessageOptions(
            role: MessageRole.Agent,
            content: "E=mc^2"
        ),
        new ThreadMessageOptions(
            role: MessageRole.User,
            content: "What is the impedance formula?"
        ),
    ]
);

do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    agentRun = client.GetRun(thread.Id, agentRun.Id);
}
while (agentRun.Status == RunStatus.Queued
    || agentRun.Status == RunStatus.InProgress);
```

Asynchronous sample:
```C# Snippet:Sample_Agent_Multiple_Messages_RunAsync
PersistentAgentThread thread = await client.CreateThreadAsync();
await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "What is the impedance formula?");

ThreadRun agentRun = await client.CreateRunAsync(
    threadId: thread.Id,
    agent.Id,
    additionalMessages: [
        new ThreadMessageOptions(
            role: MessageRole.Agent,
            content: "E=mc^2"
        ),
        new ThreadMessageOptions(
            role: MessageRole.User,
            content: "What is the impedance formula?"
        ),
    ]
);

do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    agentRun = await client.GetRunAsync(thread.Id, agentRun.Id);
}
while (agentRun.Status == RunStatus.Queued
    || agentRun.Status == RunStatus.InProgress);
```

4. Next, we print out all the messages to the console.

Synchronous sample:
```C# Snippet:Sample_Agent_Multiple_Messages_Print
PageableList<ThreadMessage> messages = client.GetMessages(thread.Id, order: ListSortOrder.Ascending);

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
```C# Snippet:Sample_Agent_Multiple_Messages_PrintAsync
PageableList<ThreadMessage> messages = await client.GetMessagesAsync(thread.Id, order:ListSortOrder.Ascending);

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

5. Clean up resources by deleting thread and agent.

Synchronous sample:
```C# Snippet:AgentsOverviewCleanupSync
client.DeleteThread(threadId: thread.Id);
client.DeleteAgent(agentId: agent.Id);
```

Asynchronous sample:
```C# Snippet:AgentsOverviewCleanup
await client.DeleteThreadAsync(threadId: thread.Id);
await client.DeleteAgentAsync(agentId: agent.Id);
```
