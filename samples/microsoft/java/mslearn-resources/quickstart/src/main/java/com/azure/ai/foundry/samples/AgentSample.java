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
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

import java.util.List;

/**
 * This sample demonstrates how to create and run an agent using the Azure AI Foundry SDK.
 */
public class AgentSample {
    public static void main(String[] args) {
        // Load configuration from .env file
        String tenantId = ConfigLoader.getAzureTenantId();
        String clientId = ConfigLoader.getAzureClientId();
        String clientSecret = ConfigLoader.getAzureClientSecret();
        String endpoint = ConfigLoader.getAzureEndpoint();
        String deploymentName = ConfigLoader.getAzureDeployment();
        
        // Create a credential object using Microsoft Entra ID
        ClientSecretCredential credential = new ClientSecretCredentialBuilder()
            .tenantId(tenantId)
            .clientId(clientId)
            .clientSecret(clientSecret)
            .build();
        
        // Create a projects client
        ProjectsClient client = new ProjectsClientBuilder()
            .credential(credential)
            .endpoint(endpoint)
            .buildClient();
        
        // Get an agent client
        AgentClient agentClient = client.getAgentClient();
        
        // Create an agent
        System.out.println("Creating agent...");
        Agent agent = agentClient.createAgent(new AgentOptions()
            .setName("Research Assistant")
            .setDescription("An agent that helps with research tasks")
            .setInstructions("You are a research assistant. Help users find information and summarize content.")
            .setModel(deploymentName));
        
        System.out.println("Agent created: " + agent.getName() + " (ID: " + agent.getId() + ")");
        
        // Create a thread for the conversation
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
