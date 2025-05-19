package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.Project;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.ai.projects.models.deployment.Deployment;
import com.azure.ai.projects.models.deployment.DeploymentOptions;

/**
 * This sample demonstrates how to create a project and deploy a model using the Azure AI Foundry SDK.
 * 
 * Projects in Azure AI Foundry are containers for AI resources, allowing you to organize and manage
 * your AI assets such as model deployments, agents, and evaluations in a structured way.
 * 
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create a new project with descriptive metadata
 * 3. How to deploy a model within the project
 * 4. How to retrieve and store project and deployment information
 * 
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT)
 */
public class CreateProject {
    public static void main(String[] args) {
        // Get the Azure endpoint from configuration
        String endpoint = ConfigLoader.getAzureEndpoint();
        
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
        
        // Create a new project with a name and description
        // Projects serve as containers for AI resources like model deployments and agents
        System.out.println("Creating project...");
        Project project = client.createProject("My Sample Project", "A project created using the Java SDK");
        
        // Display the project information for reference
        System.out.println("Project created successfully!");
        System.out.println("Project Name: " + project.getName());
        System.out.println("Project ID: " + project.getId());
        
        // Create deployment options for a model
        // This specifies which model to deploy and provides metadata
        DeploymentOptions deploymentOptions = new DeploymentOptions()
            .setName("my-deployment")
            .setModel("gpt-4") // Specify the model to deploy
            .setDescription("Sample model deployment");

        // Deploy the model in the project we just created
        System.out.println("\nDeploying model...");
        Deployment deployment = client.createDeployment(project.getId(), deploymentOptions);
        
        // Display the deployment information
        System.out.println("Model deployed successfully!");
        System.out.println("Deployment Name: " + deployment.getName());
        System.out.println("Deployment ID: " + deployment.getId());
        
        // Store the project ID for later use in other samples
        System.out.println("\nSet PROJECT_ID=" + project.getId() + " in your .env file to use this project in other samples");
    }
}
