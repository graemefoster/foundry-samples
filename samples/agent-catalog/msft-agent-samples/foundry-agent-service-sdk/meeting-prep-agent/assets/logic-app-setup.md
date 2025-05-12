# Logic app flow to fetch event details from O365 calendar

### Here are the steps to create a new Logic Apps workflow for function calling.

1. In the Azure portal search box, enter logic apps, and select Logic apps.
2. On the Logic apps page toolbar, select Add.
3. On the Create Logic App page, first select the Plan type for your logic app resource. That way, only the options for that plan type appear.
4. In the Plan section, for the Plan type, select Consumption to view only the consumption logic app resource settings.
5. Provide the following information for your logic app resource: Subscription, Resource Group, Logic App name, and Region.
6. When you're ready, select Review + Create.
7. On the validation page that appears, confirm all the provided information, and select Create.
8. After Azure successfully deploys your logic app resource, select Go to resource. Or, find and select your logic app resource by typing the name in the Azure search box.
9. Open the Logic Apps workflow in designer. Select Development Tools + Logic app designer. This opens your empty workflow in designer. Or you select Blank Logic App from templates
10. Now you're ready to add one more step in the workflow. A workflow always starts with a single trigger, which specifies the condition to meet before running any subsequent actions in the workflow.
11. Your workflow is required to have a Request trigger to generate a REST endpoint, and a response action to return the response to Azure AI Foundry when this workflow is invoked.
12. Add a trigger (Request)
Select Add a trigger and then search for request trigger. Select the When an HTTP request is received operation.

![image](https://github.com/user-attachments/assets/0221d407-e7c8-477a-8fcd-316fbaa5f1ca)

Provide the JSON schema for the request. If you do not have the schema use the option to generate schema

![image](https://github.com/user-attachments/assets/5593f822-d0b0-4690-ba98-613d75608478)

The schema used in this sample:

```
{
  "type": "object",
  "properties": {
    "start_date": {
      "type": "string",
      "format": "date-time",
      "description": "Start of the date range to filter events (ISO 8601 format)"
    },
    "end_date": {
      "type": "string",
      "format": "date-time",
      "description": "End of the date range to filter events (ISO 8601 format)"
    }
  },
  "required": [
    "start_date",
    "end_date"
  ]
}
```
Save the workflow. This will generate the REST endpoint for the workflow.

Now, create the next action in the flow - Get Events to fetch event details from the calendar (connect your account and choose the calendar). The filter query would look like:

![image](https://github.com/user-attachments/assets/c8d05d69-5eaf-452b-9685-8e35a0a43917)

Now configure the response:

![image](https://github.com/user-attachments/assets/d76937ba-e899-4d79-88bc-b5bf1ade4229)
