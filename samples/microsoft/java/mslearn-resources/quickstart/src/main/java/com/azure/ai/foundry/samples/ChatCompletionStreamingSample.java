package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.chat.ChatClient;
import com.azure.ai.projects.models.chat.ChatCompletionOptions;
import com.azure.ai.projects.models.chat.ChatCompletionStreamResponse;
import com.azure.ai.projects.models.chat.ChatMessage;
import com.azure.ai.projects.models.chat.ChatRole;
import com.azure.identity.DefaultAzureCredential;

import java.util.Arrays;
import java.util.List;

/** 
 * This sample demonstrates how to use streaming chat completion with the Azure AI Foundry SDK.
 * 
 * Streaming chat completions deliver the AI's response in real-time as it's being generated,
 * providing a more interactive experience by showing results incrementally instead of waiting
 * for the entire response to be complete.
 * 
 * This sample shows:
 * 1. How to authenticate with Azure AI Foundry using DefaultAzureCredential
 * 2. How to create a chat client for a specific model deployment
 * 3. How to structure a conversation with system and user messages
 * 4. How to configure and send a streaming chat completion request
 * 5. How to process and display the AI-generated response as it streams in
 * 
 * Streaming is particularly useful for:
 * - Creating more responsive user interfaces
 * - Supporting longer responses without timeout issues
 * - Providing real-time feedback to users
 * 
 * Prerequisites:
 * - An Azure account with access to Azure AI Foundry
 * - Azure CLI installed and logged in ('az login')
 * - Environment variables set in .env file (AZURE_ENDPOINT, AZURE_DEPLOYMENT)
 */
public class ChatCompletionStreamingSample {
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
        // This client provides access to both standard and streaming chat completion functionality
        ChatClient chatClient = client.getChatClient(deploymentName);
        
        // Create a list of chat messages to form the conversation
        // This includes a system message to set the assistant's behavior
        // and a user message containing the user's request
        List<ChatMessage> messages = Arrays.asList(
            new ChatMessage(ChatRole.SYSTEM, "You are a helpful assistant."),
            new ChatMessage(ChatRole.USER, "Write a short poem about cloud computing.")
        );
        
        // Configure chat completion options including the messages, temperature, and token limit
        // The same options structure is used for both streaming and non-streaming requests
        ChatCompletionOptions options = new ChatCompletionOptions(messages)
            .setTemperature(0.7)  // Balanced between deterministic and creative
            .setMaxTokens(800);   // Limit response length
        
        System.out.println("Sending streaming chat completion request...");
        
        // Send the streaming request and prepare to receive chunks of the response
        // Unlike standard completions, streaming returns portions of the response as they're generated
        System.out.println("\nResponse from assistant (streaming):");
        chatClient.getChatCompletionStream(options)
            .forEach(response -> {
                ChatCompletionStreamResponse delta = response;
                if (delta.getChoices() != null && !delta.getChoices().isEmpty()) {
                    String content = delta.getChoices().get(0).getDelta().getContent();
                    if (content != null) {
                        System.out.print(content);
                    }
                }
            });
        
        System.out.println("\n\nStreaming completed!");
    }
}
