package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.agent.Agent;
import com.azure.ai.projects.models.agent.AgentClient;
import com.azure.ai.projects.models.agent.AgentMessage;
import com.azure.ai.projects.models.agent.AgentOptions;
import com.azure.ai.projects.models.agent.AgentRole;
import com.azure.ai.projects.models.agent.AgentRun;
import com.azure.ai.projects.models.agent.AgentRunStatus;
import com.azure.ai.projects.models.agent.AgentThread;
import com.azure.identity.DefaultAzureCredential;
 
import java.util.List;

/**
 * This sample demonstrates how to create and run an agent using the Azure AI Foundry SDK.
 * 
 * Agents in Azure AI Foundry are specialized AI assistants that can be customized with
 * specific instructions and capabilities to perform particular tasks. They maintain conversation
 * history in threads and can be deployed for various use cases.
 * 
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create an agent with specific instructions and capabilities
 * 3. How to create a thread for conversation with the agent
 * 4. How to send messages to the agent and run it
 * 5. How to wait for the agent to complete its execution
 * 6. How to retrieve and display the agent's response
 * 
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT, AZURE_DEPLOYMENT)
 */
public class AgentSample {
    public static void main(String[] args) {
        // Load configuration values from the .env file
        // These include the service endpoint and the deployment name of the model to use
        String endpoint = ConfigLoader.getAzureEndpoint();
        String deploymentName = ConfigLoader.getAzureDeployment();
        
        // Get DefaultAzureCredential for authentication
        // This uses the most appropriate authentication method based on the environment
        // For local development, it will use your Azure CLI login credentials
        DefaultAzureCredential credential = ConfigLoader.getDefaultCredential();
        
        // Create a projects client to interact with Azure AI Foundry services
        // The client requires an authentication credential and an endpoint
        ProjectsClient client = new ProjectsClientBuilder()
            .credential(credential)
            .endpoint(endpoint)
            .buildClient();
        
        // Get an agent client, which provides operations for working with AI agents
        // This includes creating, configuring, and running agents
        AgentClient agentClient = client.getAgentClient();
        
        // Create a new agent with specialized capabilities and instructions
        // The agent is configured with a name, description, instructions, and underlying model
        System.out.println("Creating agent...");
        Agent agent = agentClient.createAgent(new AgentOptions()
            .setName("Research Assistant")                       // Descriptive name for the agent
            .setDescription("An agent that helps with research tasks")  // Brief description of the agent's purpose
            .setInstructions("You are a research assistant. Help users find information and summarize content.") // Detailed instructions for the agent's behavior
            .setModel(deploymentName));                          // The underlying AI model to power the agent
        
        System.out.println("Agent created: " + agent.getName() + " (ID: " + agent.getId() + ")");
        
        // Create a thread for the conversation with the agent
        // Threads maintain conversation history and state across multiple interactions
        System.out.println("Creating thread...");
        AgentThread thread = agentClient.createThread();
        System.out.println("Thread created: " + thread.getId());
        
        // Create a user message
        AgentMessage userMessage = new AgentMessage()
            .setRole(AgentRole.USER)
            .setContent("Explain what cloud computing is and list three benefits.");
        
        // Run the agent
        System.out.println("Running agent...");
        AgentRun run = agentClient.createRun(thread.getId(), agent.getId(), userMessage);
        System.out.println("Run created: " + run.getId());
        
        // Wait for the run to complete
        AgentRun completedRun = waitForRunCompletion(agentClient, thread.getId(), run.getId());
        System.out.println("Run completed with status: " + completedRun.getStatus());
        
        // Get messages from the thread
        List<AgentMessage> messages = agentClient.getMessages(thread.getId());
        
        // Display the assistant's response
        System.out.println("\nConversation:");
        for (AgentMessage message : messages) {
            System.out.println(message.getRole() + ": " + message.getContent());
        }
    }
    
    private static AgentRun waitForRunCompletion(AgentClient agentClient, String threadId, String runId) {
        AgentRun run = agentClient.getRun(threadId, runId);
        
        while (run.getStatus() == AgentRunStatus.QUEUED || run.getStatus() == AgentRunStatus.IN_PROGRESS) {
            try {
                System.out.println("Run status: " + run.getStatus() + " - waiting...");
                Thread.sleep(1000); // Wait for 1 second before checking again
                run = agentClient.getRun(threadId, runId);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Thread was interrupted", e);
            }
        }
        
        return run;
    }
}
