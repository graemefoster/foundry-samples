package com.azure.ai.foundry.samples;

import com.azure.ai.foundry.samples.utils.ConfigLoader;
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.ai.projects.models.chat.ChatClient;
import com.azure.ai.projects.models.chat.ChatCompletionOptions;
import com.azure.ai.projects.models.chat.ChatCompletionStreamResponse;
import com.azure.ai.projects.models.chat.ChatMessage;
import com.azure.ai.projects.models.chat.ChatRole;
import com.azure.core.credential.AzureKeyCredential;

import java.util.Arrays;
import java.util.List;

/**
 * This sample demonstrates how to use streaming chat completion with the Azure AI Foundry SDK.
 */
public class ChatCompletionStreamingSample {
    public static void main(String[] args) {
        // Load configuration from .env file
        String apiKey = ConfigLoader.getAzureApiKey();
        String endpoint = ConfigLoader.getAzureEndpoint();
        String deploymentName = ConfigLoader.getAzureDeployment();
        
        // Create a projects client
        ProjectsClient client = new ProjectsClientBuilder()
            .credential(new AzureKeyCredential(apiKey))
            .endpoint(endpoint)
            .buildClient();
        
        // Get a chat client
        ChatClient chatClient = client.getChatClient(deploymentName);
        
        // Create chat messages
        List<ChatMessage> messages = Arrays.asList(
            new ChatMessage(ChatRole.SYSTEM, "You are a helpful assistant."),
            new ChatMessage(ChatRole.USER, "Write a short poem about cloud computing.")
        );
        
        // Set chat completion options
        ChatCompletionOptions options = new ChatCompletionOptions(messages)
            .setTemperature(0.7)
            .setMaxTokens(800);
        
        System.out.println("Sending streaming chat completion request...");
        
        // Get streaming chat completion
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
