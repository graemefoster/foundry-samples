package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.Project;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

/**
 * This sample demonstrates how to create a project using the Azure AI Foundry SDK.
 */
public class CreateProject {
    public static void main(String[] args) {
        // Load configuration from .env file
        String tenantId = ConfigLoader.getAzureTenantId();
        String clientId = ConfigLoader.getAzureClientId();
        String clientSecret = ConfigLoader.getAzureClientSecret();
        String endpoint = ConfigLoader.getAzureEndpoint();
        
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
        
        // Create a project
        System.out.println("Creating project...");
        Project project = client.createProject("My Sample Project", "A project created using the Java SDK");
        
        // Display the project information
        System.out.println("Project created successfully!");
        System.out.println("Project Name: " + project.getName());
        System.out.println("Project ID: " + project.getId());
        System.out.println("Description: " + project.getDescription());
        System.out.println("Created At: " + project.getCreatedAt());
        
        // Store the project ID for later use
        System.out.println("\nSet PROJECT_ID=" + project.getId() + " in your .env file to use this project in other samples");
    }
}
