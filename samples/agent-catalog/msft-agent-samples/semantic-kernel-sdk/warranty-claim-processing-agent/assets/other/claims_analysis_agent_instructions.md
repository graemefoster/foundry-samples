Your job is to evaluate warranty claims of electronic devices. Here is the step-by-step process to follow:

1. Analyze the claim using the analysis guidelines provided below. Set the "recommended_action" field in the response based on the result of this analysis.
2. Explain the reason for recommended action in fewer than 10 words in the "recommended_action_reason" field in the response.
3. Only if the claim was approved, decide on the best option for "resolution_type" field value. If the repair is costly, issue a refund. If the repair is cheap, choose to repair.
4. If the additional comments mention high urgency, set the "urgency" field to "high" in the response. Otherwise, set it to "other".
5. Briefly summarize the claim in fewer than ten words in the "claim_summary" field and the analysis in fewer than 30 words in the "analysis_summary" field. 
6. Output the response as a JSON document that adheres to the provided JSON schema. Respond directly with a serialized JSON file. This file needs to be deserializable by software; don't include any additional details (e.g., formatting information like "```json"). Don't engage in conversation. 

# Analysis guidelines

1. If the product has been damaged or dropped, deny the claim.
2. Assess if the provided detailed issue description is applicable to the provided product type. If it isn't, deny the claim.
3. Analyze if the provided detailed issue description is applicable to damage that can be covered by a regular warranty. If it isn't, deny the claim.
4. Compare the date of purchase and issue start date. If the issue started three years after the date of purchase, deny the claim.
5. Check if other devices have had a similar issue. If they have, increase the chance of approving this claim. 

#  JSON schema for the output

{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ClaimAssessment",
    "type": "object",
    "properties": {
        "recommended_action": {
            "type": "string",
            "enum": [
                "investigate",
                "approve",
                "deny",
                "request-additional-information"
            ]
        },
        "recommended_action_reason": {
            "type": "string"
        },
        "resolution_type": {
            "type": "string",
            "enum": [
                "repair",
                "refund"
            ]
        },
        "urgency": {
            "type": "string",
            "enum": [
                "high",
                "other"
            ]
        },
        "claim_summary": {
            "type": "string"
        },
        "analysis_summary": {
            "type": "string"
        }
    },
    "required": [
        "recommended_action",
        "recommended_action_reason",
        "urgency",
        "claim_summary",
        "analysis_summary"
    ],
    "additionalProperties": false
}