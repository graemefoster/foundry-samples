import { DefaultAzureCredential } from '@azure/identity';
import { AIProjectClient } from '@azure/ai-projects';
import { AgentsClient } from '@azure/ai-agents';
import { config } from 'dotenv';
config(); 

async function chatCompletion() {
    // <chat_completion>
    const endpoint = process.env.INFERENCE_ENDPOINT;
    const deployment = process.env.MODEL_DEPLOYMENT_NAME || 'gpt-4o';
    const project = new AIProjectClient(endpoint, new DefaultAzureCredential());

    const client = project.inference.azureOpenAI();

    const chatCompletion = await client.chat.completions.create({
        deployment,
        messages: [
            { role: "system", content: "You are a helpful writing assistant" },
            { role: "user", content: "Write me a poem about flowers" },
        ],
    });
  
    console.log("response = ", JSON.stringify(chatCompletion, null, 2));
    // </chat_completion>
}

chatCompletion().catch(console.error);

async function runAgent() {
    // <create_and_run_agent>

    // Create an Azure AI Client
    const endpoint = process.env.PROJECT_ENDPOINT;
    const deployment = process.env.MODEL_DEPLOYMENT_NAME || 'gpt-4o';
    const client = new AgentsClient(endpoint, new DefaultAzureCredential());

    // Create an Agent
    const agent = await client.createAgent(deployment, {
        name: 'my-agent',
        instructions: 'You are a helpful agent',
    });

    // Create a thread and mesage
    const thread = await client.createThread();
    const message = await client.createMessage(thread.id, 'user', 'hello, world!');

    console.log(`Created message, message ID: ${message.id}`);

    // Create run
    let run = await client.createRun(thread.id, agent.id);
    console.log(`Usage for run ${run.id}:`, JSON.stringify(run.usage, null, 2));

    // Wait for run to complete
    while (['queued', 'in_progress', 'requires_action'].includes(run.status)) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        run = await client.getRun(thread.id, run.id);
        console.log(`Run status: ${run.status}`);
    }

    console.log(`Usage for run ${run.id}:`, JSON.stringify(run.usage, null, 2));

    // Delete the Agent
    await client.deleteAgent(agent.id);
    console.log(`Deleted Agent, Agent ID: ${agent.id}`);
    // </create_and_run_agent>
}

runAgent().catch(console.error);
