# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import asyncio
from dotenv import load_dotenv

from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings

from src.video_translation_plugin import VideoTranslationPlugin

load_dotenv()
        
async def main() -> None:
    ai_agent_settings = AzureAIAgentSettings.create()
    
    print("Starting Video Translation Agent...")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)

    async with (
        AsyncDefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        # 1. Create an agent on the Azure AI agent service
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name="Video_Translation_Agent",
            instructions="""
            You are a helpful video translation agent. Help users translate their videos from one language to another.
            
            When a user wants to translate a video, determine whether they have a local video file or a remote URL:
            
            For local video files:
            1. First, offer to upload their local video file to Azure Blob Storage
            2. Use the upload_to_azure_blob function to get a secure URL for the video
            3. Use the generated SAS URL as the video_url for the translation request
            
            For remote video URLs:
            1. Use the provided URL directly for the translation request
            2. Make sure the URL is accessible (has necessary SAS token if from Azure Storage)
            
            In either case, gather the following information:
            1. Source language
            2. Target language 
            3. Voice kind (PlatformVoice or PersonalVoice)

            The speaker count, subtitle max char count, and export subtitle in video are optional parameters and do not need to be provided by the user.
            
            After submitting a translation request:
            - Always provide the Translation ID to the user for reference
            - Explain that the translation process takes time to complete
            - Tell users they can check the status of their translation using the ID
            - Share the URLs for the translated video and subtitle files when available
            
            You can also help users:
            - List their translations (It might be helpful to ask if they want to see all translations, a specific number of translations, or translations with a specific criteria)
            - Get details about specific translations
            - Create iterations with WebVTT files
            - Delete translations
            
            Be friendly, helpful, and guide users through the process. Always check whether they're working with a local file or remote URL first, and adapt your approach accordingly.
            """,
        )

        # 2. Create a Semantic Kernel agent for the Azure AI agent
        agent = AzureAIAgent(
            client=client,
            definition=agent_definition,
            plugins=[VideoTranslationPlugin()],  # Add the video translation plugin
        )

        # 3. Create a thread for the agent
        thread = None

        try:
            print("Video Translation Agent is ready! How can I help you translate your videos today?")
            
            while True:
                # Get user input from console
                user_input = input("\nYou: ")
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit"]:
                    print("Ending conversation...")
                    break
                
                print("Agent is processing...")
                # 4. Invoke the agent for the specified thread for response:
                async for response in agent.invoke(
                    messages=user_input,
                    thread=thread,
                ):
                    # Don't print tool messages, only agent responses
                    if response.name != "Tool":
                        print(f"\nAgent: {response}")
                        thread = response.thread
                    
        finally:
            # 5. Cleanup: Delete the thread and agent
            print("\nCleaning up resources...")
            await thread.delete() if thread else None
            await client.agents.delete_agent(agent.id)
            print("Done!")


if __name__ == "__main__":
    asyncio.run(main())