using Azure;
using Azure.Identity;
using Azure.AI.Inference;
using Azure.Core;
using Azure.Core.Pipeline;


namespace AiAgentsTests
{
    public class SimpleInference
    {
        public static void Main(string[] args)
        {
            
            var endpointUrl = Evironment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
            var modelName = Evironment.GetEnvironmentVariable("AZURE_OPENAI_MODEL_NAME");

            var endpoint = new Uri(endpointUrl);
            var credential = new DefaultAzureCredential();
            var model = modelName;

            AzureAIInferenceClientOptions clientOptions = new AzureAIInferenceClientOptions();
            BearerTokenAuthenticationPolicy tokenPolicy = new BearerTokenAuthenticationPolicy(credential, new string[] { "https://cognitiveservices.azure.com/.default" });
            clientOptions.AddPolicy(tokenPolicy, HttpPipelinePosition.PerRetry);


            var client = new ChatCompletionsClient(
                endpoint,
                credential,
                clientOptions
            );

            var requestOptions = new ChatCompletionsOptions()
            {
                Messages =
                {
                    new ChatRequestSystemMessage("You are a helpful assistant."),
                    new ChatRequestUserMessage("How many feet are in a mile?"),
                },
            };

            Response<ChatCompletions> response = client.Complete(requestOptions);
            Console.WriteLine(response.Value.Content);
 
        }
    }
}