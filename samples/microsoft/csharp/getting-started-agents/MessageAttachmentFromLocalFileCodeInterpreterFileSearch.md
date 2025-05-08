# Sample file search on agent with message attachment and code interpreter in Azure.AI.Agents

In this example we demonstrate, how to use file search with `MessageAttachment`.

1. First we need to create agent client and read the environment variables, which will be used in the next steps.
```C# Snippet:AgentsCodeInterpreterFileAttachment_CreateClient
var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];

PersistentAgentsClient client = new(new Uri(projectEndpoint), new DefaultAzureCredential());

CodeInterpreterToolDefinition codeInterpreterTool = new();

string fileName = "sample_file_for_upload.txt";
string fullPath = Path.Combine(AppContext.BaseDirectory, fileName);

File.WriteAllText(
    path: fullPath,
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
```

2. We need to create an agent, create and upload file and `ThreadMessage` with the uploaded file ID in the `MessageAttachment`.

Synchronous sample:
```C# Snippet:AgentsCreateAgentWithInterpreterToolSync
PersistentAgent agent = client.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "You are a helpful agent that can help fetch data from files you know about.",
    tools: [codeInterpreterTool]);

PersistentAgentFile uploadedAgentFile = client.UploadFile(
    filePath: fullPath,
    purpose: PersistentAgentFilePurpose.Agents);

var fileId = uploadedAgentFile.Id;

var attachment = new MessageAttachment(
    fileId: fileId,
    tools: [codeInterpreterTool]
);

PersistentAgentThread thread = client.CreateThread();

client.CreateMessage(
    threadId: thread.Id,
    role: MessageRole.User,
    content: "Can you give me the documented codes for 'banana' and 'orange'?",
    attachments: [attachment]);
```

Asynchronous sample:
```C# Snippet:AgentsCreateAgentWithInterpreterTool
PersistentAgent agent = await client.CreateAgentAsync(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "You are a helpful agent that can help fetch data from files you know about.",
    tools: [codeInterpreterTool]);

PersistentAgentFile uploadedAgentFile = await client.UploadFileAsync(
    filePath: "sample_file_for_upload.txt",
    purpose: PersistentAgentFilePurpose.Agents);

var fileId = uploadedAgentFile.Id;

var attachment = new MessageAttachment(
    fileId: fileId,
    tools: [codeInterpreterTool]);

PersistentAgentThread thread = await client.CreateThreadAsync();

await client.CreateMessageAsync(
    threadId: thread.Id,
    role: MessageRole.User,
    content: "Can you give me the documented codes for 'banana' and 'orange'?",
    attachments: [attachment]);
```

3. Next we will create a `ThreadRun` and wait until the run is completed. If the run was not successful we will print the last error message.

Synchronous sample:
```C# Snippet:AgentsCodeInterpreterFileAttachmentSync_CreateRun
ThreadRun run = client.CreateRun(
    thread.Id,
    agent.Id);

do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

Asynchronous sample:
```C# Snippet:AgentsCodeInterpreterFileAttachmentSync_CreateRun
ThreadRun run = await client.CreateRunAsync(
    thread.Id,
    agent.Id);

do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = await client.GetRunAsync(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

4. Print the messages to the console in chronological order.

Synchronous sample:
```C# Snippet:AgentsCodeInterpreterFileAttachmentSync_PrintMessages
PageableList<ThreadMessage> messages = client.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending);

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
```C# Snippet:AgentsCodeInterpreterFileAttachment_PrintMessages
PageableList<ThreadMessage> messages = await client.GetMessagesAsync(
    threadId: thread.Id,
    order: ListSortOrder.Ascending);

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

5. Finally, we delete all the resources, we have created in this sample.

Synchronous sample:
```C# Snippet:AgentsCodeInterpreterFileAttachmentSync_Cleanup
client.DeleteFile(fileId: fileId);
client.DeleteThread(thread.Id);
client.DeleteAgent(agent.Id);
```

Asynchronous sample:
```C# Snippet:AgentsCodeInterpreterFileAttachment_Cleanup
await client.DeleteFileAsync(fileId);
await client.DeleteThreadAsync(thread.Id);
await client.DeleteAgentAsync(agent.Id);
```
