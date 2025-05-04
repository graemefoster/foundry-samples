// <create_project>
import { DefaultAzureCredential } from '@azure/identity';
import { CognitiveServicesManagementClient } from '@azure/arm-cognitiveservices';
import { config } from 'dotenv';
config();

const subscriptionId = process.env.SUBSCRIPTION_ID;
const resourceGroupName = process.env.RESOURCE_GROUP_NAME;
const foundryResourceName = process.env.FOUNDRY_RESOURCE_NAME;
const foundryProjectName = process.env.FOUNDRY_PROJECT_NAME;
const location = process.env.LOCATION;

const client = new CognitiveServicesManagementClient(
  new DefaultAzureCredential(), 
  subscriptionId, {
  apiVersion: '2025-04-01-preview'
});

async function createAIFoundryProject() {  
    const account = await client.accounts.beginCreateAndWait(
      resourceGroupName,
      foundryResourceName,
      {
        location,
        kind: 'AIServices',
        sku: { name: 'S0' },
        identity: { type: 'SystemAssigned' },
        properties: { allowProjectManagement: true }
      },
      { foundryProjectName }
    );
  
    console.log('AI Foundry account created:', account);
  }

createAIFoundryProject().catch(err => {
  console.error('Error during provisioning:', err);
  process.exit(1);
});

// <create_project>

// <deploy_model>
// async function deployModel() { 
//   const deployment = await client.deployments.beginCreateOrUpdateAndWait(
//     resourceGroupName,
//     accountName,
//     deploymentName,
//     {
//       properties: {
//         model: {
//           format: 'OpenAI',
//           name: 'gpt-4o',
//           publisher: 'OpenAI'
//         }
//       },
//       sku: {
//         capacity: 1,
//         name: 'Standard'
//       }
//     }
//   );
//   console.log('Model deployed:', model);
// }

// deployModel().catch(err => {
//   console.error('Error during model deployment:', err);
//   process.exit(1);
// });
// <deploy_model
