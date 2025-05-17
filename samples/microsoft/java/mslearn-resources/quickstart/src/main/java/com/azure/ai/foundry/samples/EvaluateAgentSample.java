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
import com.azure.ai.projects.models.evaluation.AgentEvaluation;
import com.azure.ai.projects.models.evaluation.EvaluationClient;
import com.azure.ai.projects.models.evaluation.EvaluationMetric;
import com.azure.ai.projects.models.evaluation.EvaluationOptions;
import com.azure.identity.DefaultAzureCredential;

import java.util.Map;

/**
 * This sample demonstrates how to evaluate an agent run using the Azure AI Foundry SDK.
 * 
 * Evaluation in Azure AI Foundry allows you to assess the performance and quality of AI agents
 * using standardized metrics. This helps identify areas for improvement and ensures the agent
 * meets specific quality standards before deployment.
 * 
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create an agent and generate a run for evaluation
 * 3. How to use the evaluation client to assess the agent's performance
 * 4. How to select and apply appropriate evaluation metrics
 * 5. How to interpret evaluation results and scores
 * 
 * Key evaluation metrics include:
 * - Helpfulness: Measures how well the agent assists users with their requests
 * - Accuracy: Assesses the factual correctness of the agent's responses
 * - Safety: Evaluates if the agent follows appropriate content guidelines
 * - Quality: Measures overall response quality and relevance
 *  
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT, AZURE_DEPLOYMENT)
 */
public class EvaluateAgentSample {
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
        
        // Get an agent client to work with AI agents
        // This will be used to create and run the agent we're going to evaluate
        AgentClient agentClient = client.getAgentClient();
        
        // First, create and run an agent to generate a run for evaluation
        // We need an agent run to evaluate, so we'll create one as part of this sample
        System.out.println("Creating and running an agent to generate a run for evaluation...");
        
        // Create an agent with a specific purpose and capabilities
        // For evaluation, it's important to create an agent with clear instructions
        // that align with the metrics you'll be evaluating
        Agent agent = agentClient.createAgent(new AgentOptions()
            .setName("Weather Assistant")                     // Descriptive name
            .setDescription("An agent that provides weather information")  // Brief description
            .setInstructions("You are a weather assistant. Provide accurate and helpful information about weather conditions.")  // Detailed instructions
            .setModel(deploymentName));                       // The underlying AI model
        
        // Create a thread
        AgentThread thread = agentClient.createThread();
        
        // Create a user message with a specific task to evaluate
        AgentMessage userMessage = new AgentMessage()
            .setRole(AgentRole.USER)
            .setContent("What should I wear if it's going to be rainy and cold tomorrow?");
        
        // Run the agent
        AgentRun run = agentClient.createRun(thread.getId(), agent.getId(), userMessage);
        System.out.println("Run created with ID: " + run.getId());
        
        // Wait for the run to complete
        AgentRun completedRun = waitForRunCompletion(agentClient, thread.getId(), run.getId());
        System.out.println("Run completed with status: " + completedRun.getStatus());
        
        // Get the evaluation client
        EvaluationClient evaluationClient = client.getEvaluationClient();
        
        // Create an evaluation for the agent run
        System.out.println("Evaluating agent run...");
        EvaluationOptions options = new EvaluationOptions()
            .addMetric(EvaluationMetric.HELPFULNESS)
            .addMetric(EvaluationMetric.ACCURACY)
            .addMetric(EvaluationMetric.QUALITY);
        
        AgentEvaluation evaluation = evaluationClient.evaluateAgentRun(completedRun.getId(), options);
        
        // Display the evaluation results
        System.out.println("\nEvaluation Results:");
        System.out.println("Evaluation ID: " + evaluation.getId());
        System.out.println("Created At: " + evaluation.getCreatedAt());
        
        Map<EvaluationMetric, Double> scores = evaluation.getScores();
        for (Map.Entry<EvaluationMetric, Double> score : scores.entrySet()) {
            System.out.printf("%s Score: %.2f/10\n", score.getKey(), score.getValue());
        }
        
        // Display feedback
        System.out.println("\nFeedback:");
        System.out.println(evaluation.getFeedback());
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
