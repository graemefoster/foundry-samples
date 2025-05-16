package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.chat.ChatClient;
import com.azure.ai.projects.models.chat.ChatCompletion;
import com.azure.ai.projects.models.chat.ChatCompletionOptions;
import com.azure.ai.projects.models.chat.ChatMessage;
import com.azure.ai.projects.models.chat.ChatRole;
import com.azure.identity.ClientSecretCredential;
import com.azure.identity.ClientSecretCredentialBuilder;

import java.util.Arrays;
import java.util.List;

/**
 * This sample demonstrates how to use the chat completion API with the Azure AI Foundry SDK.
 */
public class ChatCompletionSample {
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
        
        // Get a chat client
        ChatClient chatClient = client.getChatClient(deploymentName);
        
        // Create chat messages
        List<ChatMessage> messages = Arrays.asList(
            new ChatMessage(ChatRole.SYSTEM, "You are a helpful assistant."),
            new ChatMessage(ChatRole.USER, "Tell me about Azure AI Foundry.")
        );
        
        // Set chat completion options
        ChatCompletionOptions options = new ChatCompletionOptions(messages)
            .setTemperature(0.7)
            .setMaxTokens(800);
        
        System.out.println("Sending chat completion request...");
        
        // Get chat completion
        ChatCompletion completion = chatClient.getChatCompletion(options);
        
        // Display the response
        System.out.println("\nResponse from assistant:");
        System.out.println(completion.getChoices().get(0).getMessage().getContent());
        
        // Display usage statistics
        System.out.println("\nUsage Statistics:");
        System.out.println("Prompt Tokens: " + completion.getUsage().getPromptTokens());
        System.out.println("Completion Tokens: " + completion.getUsage().getCompletionTokens());
        System.out.println("Total Tokens: " + completion.getUsage().getTotalTokens());
    }
}
