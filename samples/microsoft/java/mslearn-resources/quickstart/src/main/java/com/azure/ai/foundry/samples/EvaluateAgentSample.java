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
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

import java.util.Map;

/**
 * This sample demonstrates how to evaluate an agent run using the Azure AI Foundry SDK.
 */
public class EvaluateAgentSample {
    public static void main(String[] args) {
        // Load configuration from .env file
        String tenantId = ConfigLoader.getAzureTenantId();
        String clientId = ConfigLoader.getAzureClientId();
        String clientSecret = ConfigLoader.getAzureClientSecret();
        String endpoint = ConfigLoader.getAzureEndpoint();
        String deploymentName = ConfigLoader.getAzureDeployment();
        
        // Create a projects client
        ProjectsClient client = new ProjectsClientBuilder()
            .credential(new AzureKeyCredential(apiKey))
            .endpoint(endpoint)
            .buildClient();
        
        // Get an agent client
        AgentClient agentClient = client.getAgentClient();
        
        // First, create and run an agent to generate a run for evaluation
        System.out.println("Creating and running an agent to generate a run for evaluation...");
        
        // Create an agent
        Agent agent = agentClient.createAgent(new AgentOptions()
            .setName("Weather Assistant")
            .setDescription("An agent that provides weather information")
            .setInstructions("You are a weather assistant. Provide accurate and helpful information about weather conditions.")
            .setModel(deploymentName));
        
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
