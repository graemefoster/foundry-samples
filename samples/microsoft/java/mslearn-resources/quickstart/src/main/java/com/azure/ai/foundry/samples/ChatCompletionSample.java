package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.chat.ChatClient;
import com.azure.ai.projects.models.chat.ChatCompletion;
import com.azure.ai.projects.models.chat.ChatCompletionOptions;
import com.azure.ai.projects.models.chat.ChatMessage;
import com.azure.ai.projects.models.chat.ChatRole;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.ai.projects.models.chat.ChatCompletionResponse;



import java.util.Arrays;
import java.util.List;

/**
 * This sample demonstrates how to use the chat completion API with the Azure AI Foundry SDK.
 * 
 * Chat completions allow you to have interactive, conversational interactions with AI models
 * by providing a list of messages and receiving AI-generated responses that maintain context
 * across the conversation.
 * 
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create a chat client for a specific model deployment
 * 3. How to structure a conversation with system and user messages
 * 4. How to configure and send a chat completion request
 * 5. How to process and display the AI-generated response
 * 
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT, AZURE_DEPLOYMENT)
 */
public class ChatCompletionSample {
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
        
        // Get a chat client for the specified model deployment 
        // This client provides access to chat completion functionality
        ChatClient chatClient = client.getChatClient(deploymentName);
        
        // Create a list of chat messages to form the conversation
        // This includes a system message to set the assistant's behavior
        // and a user message containing the user's question or prompt
        List<ChatMessage> messages = Arrays.asList(
            new ChatMessage(ChatRole.SYSTEM, "You are a helpful assistant."),
            new ChatMessage(ChatRole.USER, "Tell me about Azure AI Foundry.")
        );
        
        // Configure chat completion options including the messages, temperature, and token limit
        // - Temperature controls randomness: lower values (like 0.2) give more focused responses,
        //   higher values (like 0.8) give more creative responses
        // - MaxTokens limits the length of the response
        ChatCompletionOptions options = new ChatCompletionOptions(messages)
            .setTemperature(0.7)  // Balanced between deterministic and creative
            .setMaxTokens(800);   // Limit response length
        
        System.out.println("Sending chat completion request...");
        
        // Send the request and get the AI-generated completion
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
