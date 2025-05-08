using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Core;
using Azure.Identity;
using System;
using System.Collections.Generic;
using System.Threading;


namespace AiAgentsTests
{

    // <create_and_run_agent>
    public class AgentService
    {
        public static void MathAgent()
        {
            var endpointUrl = Evironment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
            var modelName = Evironment.GetEnvironmentVariable("AZURE_OPENAI_MODEL_NAME");

            var endpoint = new Uri(endpointUrl);
            var credential = new DefaultAzureCredential();
            var model = modelName;

            var agentClient = new PersistentAgentsClient(
                endpoint,
                credential);

            // Create a new agent with the specified model, name, and instructions
            PersistentAgent agent = agentClient.CreateAgent(
                model: model,
                name: "Math Tutor",
                instructions: "You are a personal electronics tutor. Write and run code to answer questions.",
                tools: [new CodeInterpreterToolDefinition()]);
            
            // Create a new thread for the agent to run in
            PersistentAgentThread thread = agentClient.CreateThread();

            // Create a new run for the agent in the thread
            ThreadMessage message = agentClient.CreateMessage(
                thread.Id,
                MessageRole.User,
                "I need to solve the equation `3x + 11 = 14`. Can you help me?");

            // Create a new run for the agent in the thread with additional instructions
            ThreadRun run = agentClient.CreateRun(
                thread.Id,
                agent.Id,
                additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");

            // Wait for the run to complete
            // This is a blocking call, so it will wait until the run is completed
            do
            {
                Thread.Sleep(TimeSpan.FromMilliseconds(500));
                run = agentClient.GetRun(thread.Id, run.Id);
            }
            while (run.Status == RunStatus.Queued
                || run.Status == RunStatus.InProgress);

            // Show the run results
            PageableList<ThreadMessage> messages
                = agentClient.GetMessages(
                    threadId: thread.Id, order: ListSortOrder.Ascending);

            // Print the messages in the thread
            foreach (ThreadMessage threadMessage in messages)
            {
                Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
                foreach (MessageContent contentItem in threadMessage.ContentItems)
                {
                    if (contentItem is MessageTextContent textItem)
                    {
                        Console.Write(textItem.Text);
                    }
                    else if (contentItem is MessageImageFileContent imageFileItem)
                    {
                        Console.Write($"<image from ID: {imageFileItem.FileId}");
                    }
                    Console.WriteLine();
                }
            }

            // Delete the thread and agent after use
            agentClient.DeleteThread(threadId: thread.Id);
            agentClient.DeleteAgent(agentId: agent.Id);
        }
    }
    // </create_and_run_agent>
}