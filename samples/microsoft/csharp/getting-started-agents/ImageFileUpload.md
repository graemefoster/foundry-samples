# Sample using agents with Image File as an input in Azure.AI.Agents

Demonstrates examples of sending an image file (along with optional text) as a structured content block in a single message. The examples shows how to create an agent, open a thread, post content blocks combining text and image inputs, and then run the agent to see how it interprets the multimedia input.

1. First get `ProjectEndpoint` and `ModelDeploymentName` from config and create a `PersistentAgentsClient`.

```C# Snippet:AgentsImageFileInMessageCreateClient
var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
PersistentAgentsClient client = new(new Uri(projectEndpoint), new DefaultAzureCredential());
```

2. Upload a file for referencing in your message:

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageUpload_Sync
var completeFilePath = "C:\\Users\\username\\Downloads\\image.jpg";

PersistentAgentFile uploadedFile = client.UploadFile(
    filePath: completeFilePath,
    purpose: PersistentAgentFilePurpose.Agents
);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageUpload
var completeFilePath = "C:\\Users\\username\\Downloads\\image.jpg";

PersistentAgentFile uploadedFile = await client.UploadFileAsync(
    filePath: completeFilePath,
    purpose: PersistentAgentFilePurpose.Agents
);
```

3. Create an agent.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateAgent_Sync
PersistentAgent agent = client.CreateAgent(
    model: modelDeploymentName,
    name: "File Image Understanding Agent",
    instructions: "Analyze images from internally uploaded files."
);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateAgent
PersistentAgent agent = await client.CreateAgentAsync(
    model: modelDeploymentName,
    name: "File Image Understanding Agent",
    instructions: "Analyze images from internally uploaded files."
);
```

4. Create a thread.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateThread_Sync
PersistentAgentThread thread = client.CreateThread();
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateThread
PersistentAgentThread thread = await client.CreateThreadAsync();
```

5. Create a message referencing the uploaded file.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateMessage_Sync
var contentBlocks = new List<MessageInputContentBlock>
{
    new MessageInputTextBlock("Here is an uploaded file. Please describe it:"),
    new MessageInputImageFileBlock(new MessageImageFileParam(uploadedFile.Id))
};

client.CreateMessage(
    threadId: thread.Id,
    role: MessageRole.User,
    contentBlocks: contentBlocks
);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateMessage
var contentBlocks = new List<MessageInputContentBlock>
{
    new MessageInputTextBlock("Here is an uploaded file. Please describe it:"),
    new MessageInputImageFileBlock(new MessageImageFileParam(uploadedFile.Id))
};

await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    contentBlocks: contentBlocks
);
```

6. Run the agent.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateRun_Sync
ThreadRun run = client.CreateRun(
    threadId: thread.Id,
    assistantId: agent.Id
);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageCreateRun
ThreadRun run = await client.CreateRunAsync(
    threadId: thread.Id,
    assistantId: agent.Id
);
```

7. Wait for the run to complete.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageWaitForRun_Sync
do
{
    Thread.Sleep(500);
    run = client.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageWaitForRun
do
{
    await Task.Delay(500);
    run = await client.GetRunAsync(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);
```

8. Retrieve messages (including any agent responses) and print them.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageReview_Sync
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
```C# Snippet:AgentsImageFileInMessageReview
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

9. Finally, we delete all the resources, we have created in this sample.

Synchronous sample:
```C# Snippet:AgentsImageFileInMessageCleanup_Sync
client.DeleteThread(thread.Id);
client.DeleteAgent(agent.Id);
client.DeleteFile(uploadedFile.Id);
```

Asynchronous sample:
```C# Snippet:AgentsImageFileInMessageCleanup
await client.DeleteFileAsync(uploadedFile.Id);
await client.DeleteThreadAsync(thread.Id);
await client.DeleteAgentAsync(agent.Id);
```
