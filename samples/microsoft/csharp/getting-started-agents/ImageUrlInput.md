# Sample using agents with Image URL as an input in Azure.AI.Agents

This sample demonstrates examples of sending an image URL (along with optional text) as a structured content block in a single message. The examples shows how to create an agent, open a thread,  post content blocks combining text and image inputs, and then run the agent to see how it interprets the multimedia input.

1. First get `ProjectEndpoint` and `ModelDeploymentName` from config and create a `PersistentAgentsClient`.

```C# Snippet:AgentImageUrlInMessageCreateClient
var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
PersistentAgentsClient client = new(new Uri(projectEndpoint), new DefaultAzureCredential());
```

2. Create an agent.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateAgent_Sync
PersistentAgent agent = client.CreateAgent(
    model: modelDeploymentName,
    name: "Image Understanding Agent",
    instructions: "You are an image-understanding agent. Analyze images and provide textual descriptions."
);
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateAgent
PersistentAgent agent = await client.CreateAgentAsync(
    model: modelDeploymentName,
    name: "Image Understanding Agent",
    instructions: "You are an image-understanding agent. Analyze images and provide textual descriptions."
);
```

3. Create a thread

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateThread_Sync
PersistentAgentThread thread = client.CreateThread();
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateThread
PersistentAgentThread thread = await client.CreateThreadAsync();
```

4. Create a message using multiple content blocks. Here we combine a short text and an image URL in a single user message.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateMessage_Sync
MessageImageUrlParam imageUrlParam = new MessageImageUrlParam(
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
);
imageUrlParam.Detail = ImageDetailLevel.High;

var contentBlocks = new List<MessageInputContentBlock>
{
    new MessageInputTextBlock("Could you describe this image?"),
    new MessageInputImageUrlBlock(imageUrlParam)
};

client.CreateMessage(
    threadId: thread.Id,
    role: MessageRole.User,
    contentBlocks: contentBlocks
);
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateMessage
MessageImageUrlParam imageUrlParam = new MessageImageUrlParam(
    url: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
);
imageUrlParam.Detail = ImageDetailLevel.High;
var contentBlocks = new List<MessageInputContentBlock>
{
    new MessageInputTextBlock("Could you describe this image?"),
    new MessageInputImageUrlBlock(imageUrlParam)
};

await client.CreateMessageAsync(
    threadId: thread.Id,
    role: MessageRole.User,
    contentBlocks: contentBlocks
);
```

5. Run the agent against the thread that now has an image to analyze.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateRun_Sync
ThreadRun run = client.CreateRun(
    threadId: thread.Id,
    assistantId: agent.Id
);
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageCreateRun
ThreadRun run = await client.CreateRunAsync(
    threadId: thread.Id,
    assistantId: agent.Id
);
```

6. Wait for the run to complete.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageWaitForRun_Sync
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageWaitForRun
do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    run = await client.GetRunAsync(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);
```

7. Retrieve messages (including how the agent responds) and print their contents.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageReview_Sync
PageableList<ThreadMessage> messages = client.GetMessages(
    thread.Id,
    order: ListSortOrder.Ascending);

foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.Write($"{threadMessage.Role}: {textItem.Text}");
                Console.WriteLine();
                break;

            case MessageImageFileContent fileItem:
                Console.WriteLine($"{threadMessage.Role}:  Image File (internal ID): {fileItem.FileId}");
                Console.WriteLine();
                break;
        }
    }
}
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageReview
PageableList<ThreadMessage> messages = await client.GetMessagesAsync(
    thread.Id,
    order: ListSortOrder.Ascending);

foreach (ThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.Write($"{threadMessage.Role}: {textItem.Text}");
                Console.WriteLine();
                break;

            case MessageImageFileContent fileItem:
                Console.WriteLine($"{threadMessage.Role}:  Image File (internal ID): {fileItem.FileId}");
                Console.WriteLine();
                break;
        }
    }
}
```

8. Finally, we delete all the resources, we have created in this sample.

Synchronous sample:
```C# Snippet:AgentImageUrlInMessageCleanup_Sync
client.DeleteThread(thread.Id);
client.DeleteAgent(agent.Id);
```

Asynchronous sample:
```C# Snippet:AgentImageUrlInMessageCleanup
await client.DeleteThreadAsync(thread.Id);
await client.DeleteAgentAsync(agent.Id);
```
