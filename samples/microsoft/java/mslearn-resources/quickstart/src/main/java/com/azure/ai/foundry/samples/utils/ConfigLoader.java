package com.azure.ai.foundry.samples.utils;

import io.github.cdimascio.dotenv.Dotenv;

/**
 * Utility class for loading configuration from .env file
 */
public class ConfigLoader {
    private static final Dotenv dotenv = Dotenv.configure().ignoreIfMissing().load();

    /**
     * Get an environment variable
     * 
     * @param key The environment variable key
     * @return The environment variable value
     */
    public static String getVariable(String key) {
        return dotenv.get(key);
    }

    /**
     * Get an environment variable with a default value
     * 
     * @param key The environment variable key
     * @param defaultValue The default value if the key is not found
     * @return The environment variable value or the default value
     */
    public static String getVariable(String key, String defaultValue) {
        String value = dotenv.get(key);
        return value != null ? value : defaultValue;
    }

    /**
     * Get the Azure API Key
     * 
     * @return The Azure API Key
     */
    public static String getAzureApiKey() {
        return getVariable("AZURE_API_KEY");
    }

    /**
     * Get the Azure Endpoint
     * 
     * @return The Azure Endpoint
     */
    public static String getAzureEndpoint() {
        return getVariable("AZURE_ENDPOINT");
    }

    /**
     * Get the Azure Deployment Name
     * 
     * @return The Azure Deployment Name
     */
    public static String getAzureDeployment() {
        return getVariable("AZURE_DEPLOYMENT");
    }

    /**
     * Get the Project ID (optional)
     * 
     * @return The Project ID
     */
    public static String getProjectId() {
        return getVariable("PROJECT_ID", null);
    }
}
