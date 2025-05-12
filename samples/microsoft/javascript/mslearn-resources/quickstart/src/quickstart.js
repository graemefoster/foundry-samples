import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { DefaultAzureCredential } from '@azure/identity';
import { AIProjectClient } from '@azure/ai-projects';
import { AgentsClient, ToolUtility, DoneEvent, ErrorEvent, RunStreamEvent, MessageStreamEvent } from '@azure/ai-agents';
import { config } from 'dotenv';
config();

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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

// chatCompletion().catch(console.error);

async function runAgents() {
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
    console.log(`\n==================== 🕵️  POEM AGENT ====================`);

    // Create a thread and message
    const thread = await client.createThread();
    const prompt = 'Write me a poem about flowers';
    console.log(`\n---------------- 📝 User Prompt ---------------- \n${prompt}`);
    await client.createMessage(thread.id, 'user', prompt);

    // Create run
    let run = await client.createRun(thread.id, agent.id);

    // Wait for run to complete
    console.log(`\n---------------- 🚦 Run Status ----------------`);
    while (['queued', 'in_progress', 'requires_action'].includes(run.status)) {
        // Avoid adding a lot of messages to the console
        await new Promise((resolve) => setTimeout(resolve, 1000));
        run = await client.getRun(thread.id, run.id);
        console.log(`Run status: ${run.status}`);
    }

    console.log('\n---------------- 📊 Token Usage ----------------');
    console.table([run.usage]);

    const messages = await client.listMessages(thread.id);
    const assistantMessage = messages.data.find(m => m.role === 'assistant');
    console.log('\n---------------- 💬 Response ----------------');
    printAssistantMessage(assistantMessage);

    // Delete the Agent
    await client.deleteAgent(agent.id);
    console.log(`Deleted Agent, Agent ID: ${agent.id}`);

    // </create_and_run_agent>

    // <create_filesearch_agent> 

    // Upload a file named product_info_1.md
    console.log(`\n==================== 🕵️  FILE AGENT ====================`);
    const filePath = path.join(__dirname, '../../../../data/product_info_1.md');
    const fileStream = fs.createReadStream(filePath);
    const file = await client.uploadFile(fileStream, 'assistants', {
        fileName: 'product_info_1.md'
    });
    console.log(`Uploaded file, ID: ${file.id}`);
    const vectorStore = await client.createVectorStore({
        fileIds: [file.id],
        name: 'my_vectorstore'
    });
    console.log('\n---------------- 🗃️ Vector Store Info ----------------');
    console.table([
        {
            'Vector Store ID': vectorStore.id,
            'Usage (bytes)': vectorStore.usageBytes,
            'File Count': vectorStore.fileCounts?.total ?? 'N/A'
        }
    ]);

    // Create an Agent and a FileSearch tool
    const fileSearchTool = ToolUtility.createFileSearchTool([vectorStore.id]);
    const fileAgent = await client.createAgent(deployment, {
        name: 'my-file-agent',
        instructions: 'You are a helpful assistant and can search information from uploaded files',
        tools: [fileSearchTool.definition],
        toolResources: fileSearchTool.resources,
    });

    // Create a thread and message
    const fileSearchThread = await client.createThread({ toolResources: fileSearchTool.resources });
    const filePrompt = 'What are the steps to setup the TrailMaster X4 Tent?';
    console.log(`\n---------------- 📝 User Prompt ---------------- \n${filePrompt}`);
    await client.createMessage(fileSearchThread.id, 'user', filePrompt);

    // Create run
    let fileSearchRun = await client.createRun(fileSearchThread.id, fileAgent.id).stream();

    for await (const eventMessage of fileSearchRun) {
        switch (eventMessage.event) {
            case RunStreamEvent.ThreadRunCreated:
                break;
            case MessageStreamEvent.ThreadMessageDelta:
                {
                    const messageDelta = eventMessage.data;
                    messageDelta.delta.content.forEach((contentPart) => {
                        if (contentPart.type === "text") {
                            const textContent = contentPart;
                            const textValue = textContent.text?.value || "No text";
                        }
                    });
                }
                break;

            case RunStreamEvent.ThreadRunCompleted:
                break;
            case ErrorEvent.Error:
                console.log(`An error occurred. Data ${eventMessage.data}`);
                break;
            case DoneEvent.Done:
                break;
        }
    }

    const fileSearchMessages = await client.listMessages(fileSearchThread.id);
    const fileAssistantMessage = fileSearchMessages.data.find(m => m.role === 'assistant');
    console.log(`\n---------------- 💬 Response ---------------- \n`);
    printAssistantMessage(fileAssistantMessage);

    client.deleteVectorStore(vectorStore.id);
    client.deleteFile(file.id);
    client.deleteAgent(fileAgent.id);
    console.log(`\n🧹 Deleted VectorStore, File, and FileAgent. FileAgent ID: ${fileAgent.id}`);

    // </create_filesearch_agent>
}

runAgents().catch(console.error);

// Helper function to print assistant message content nicely (handles nested text.value)
function printAssistantMessage(message) {
    if (!message || !Array.isArray(message.content)) {
        console.log('No assistant message found or content is not in expected format.');
        return;
    }
    let output = message.content.map(c => {
        if (typeof c.text === 'object' && c.text.value) {
            return c.text.value;
        } else if (typeof c.text === 'string') {
            return c.text;
        } else {
            return JSON.stringify(c);
        }
    }).join('');
    if (typeof output !== 'string') {
        console.log('Value is not a string:', output);
        return;
    }
    output.split('\n').forEach(line => console.log(line));
}
