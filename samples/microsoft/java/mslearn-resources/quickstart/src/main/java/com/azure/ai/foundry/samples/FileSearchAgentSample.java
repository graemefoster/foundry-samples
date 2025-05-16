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
import com.azure.ai.projects.models.agent.FileTool;
import com.azure.ai.projects.models.file.File;
import com.azure.ai.projects.models.file.FileClient;
import com.azure.identity.DefaultAzureCredential;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/**
 * This sample demonstrates how to create an agent with file search capability using the Azure AI Foundry SDK.
 * 
 * File search agents can analyze and extract information from documents, allowing users to ask
 * questions about the content of those documents. This extends the capabilities of regular agents
 * by giving them access to specific information contained in files.
 *  
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create and upload a sample document
 * 3. How to create an agent with file search capabilities
 * 4. How to configure the agent with access to specific files
 * 5. How to run the agent and ask questions about the document content
 * 6. How to retrieve and display the agent's responses
 * 
 * Use cases for file search agents include:
 * - Document analysis and summarization
 * - Question answering from technical documentation
 * - Data extraction from structured files
 * - Research assistance across multiple documents
 * 
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT, AZURE_DEPLOYMENT)
 */
public class FileSearchAgentSample {
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
        
        try {
            // Create a sample document containing information about cloud computing
            // In a real application, you would use your own existing documents
            Path tempFile = createSampleDocument();
            
            // Get a file client to handle file operations
            // This is used to upload files that the agent will search through
            FileClient fileClient = client.getFileClient();
            
            // Upload the file to Azure AI Foundry
            // The uploaded file will be available for the agent to search and analyze
            System.out.println("Uploading file: " + tempFile);
            File uploadedFile = fileClient.uploadFile(tempFile.toString());
            System.out.println("File uploaded with ID: " + uploadedFile.getId());
            
            // Get an agent client
            AgentClient agentClient = client.getAgentClient();
            
            // Create an agent with file search capability
            System.out.println("Creating agent with file search capability...");
            Agent agent = agentClient.createAgent(new AgentOptions()
                .setName("Document Assistant")
                .setDescription("An agent that helps with document searching")
                .setInstructions("You are a document assistant. Help users find information in their documents.")
                .setModel(deploymentName)
                .addTool(new FileTool()
                    .addFile(uploadedFile.getId())));
            
            System.out.println("Agent created: " + agent.getName() + " (ID: " + agent.getId() + ")");
            
            // Create a thread for the conversation
            System.out.println("Creating thread...");
            AgentThread thread = agentClient.createThread();
            System.out.println("Thread created: " + thread.getId());
            
            // Create a user message
            AgentMessage userMessage = new AgentMessage()
                .setRole(AgentRole.USER)
                .setContent("Find and list the benefits of cloud computing from my document.");
            
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
            
            // Clean up the temporary file
            Files.deleteIfExists(tempFile);
            
        } catch (IOException e) {
            System.err.println("Error working with files: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static Path createSampleDocument() throws IOException {
        String content = "# Cloud Computing Overview\n\n" +
                "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet ("the cloud") to offer faster innovation, flexible resources, and economies of scale.\n\n" +
                "## Benefits of Cloud Computing\n\n" +
                "1. **Cost Savings**: Cloud computing eliminates the capital expense of buying hardware and software and setting up and running on-site data centers.\n\n" +
                "2. **Scalability**: Cloud services can be scaled up or down based on demand, providing businesses with flexibility as their needs change.\n\n" +
                "3. **Performance**: The biggest cloud computing services run on a worldwide network of secure data centers, which are regularly upgraded to the latest generation of fast and efficient computing hardware.\n\n" +
                "4. **Reliability**: Cloud computing makes data backup, disaster recovery, and business continuity easier and less expensive because data can be mirrored at multiple redundant sites on the cloud provider's network.\n\n" +
                "5. **Security**: Many cloud providers offer a broad set of policies, technologies, and controls that strengthen your security posture overall.";
        
        Path tempFile = Files.createTempFile("cloud-computing-info-", ".md");
        Files.writeString(tempFile, content);
        return tempFile;
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
