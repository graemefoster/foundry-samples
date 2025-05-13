{
  "states": [
    {
      "name": "Authentication",
      "description": "Authentication phase of the workflow",
      "actors": [
        {
          "agent": "CustomerAuthenticator",          
          "outputs": 
            {
               "CustomerAccount" : "CustomerId"
            },
          "thread": "",
          "maxTurn": null,
          "humanInLoopMode": "onNoMessage",
          "streamOutput": true
        }
      ],
      "isFinal": false
    },
    {
      "name": "Billing",
      "description": "Billing phase of the workflow.",
      "actors": [
        {
          "agent": "BillingAgent",          
          "inputs":
            {
              "accountNumber":"CustomerId"
            },
          "thread": "",
          "maxTurn": null,
          "humanInLoopMode": "onNoMessage",
          "streamOutput": true
        }
      ],
      "isFinal": false
    },
    {
      "name": "End",
      "description": "Terminal State OF the workflow",
      "actors": [],
      "isFinal": true
    }
  ],
  "transitions": [
    {
      "from": "Authentication",
      "to": "Billing",
      "event": "CustomerValidated"
    },
    {
      "from": "Billing",
      "to": "End",
      "event": "ConversationEnd"
    }
  ],
  "variables": [    
    {
      "Type": "userDefined",
      "name": "CustomerId"
    }
  ],
  "startstate": "Authentication"
}