# One-time Calendy Link generator

This application  generates a One-time access link to book calls using [Calendly](https://calendly.com/). Includes a REST API to fetch the access links from Calendly.

## Installation

```bash
pip install requirements.txt
```
### Prerequisites
- Add your Freshdesk credentials as a environmental variable labelled `FRESHDESK_AGENT_API_KEY`.
-  Add the event ID in the `event_id` variable and headers for the Calendly request in the `headers` dictionary. 
- Make sure to add the URL of the API endpoint in the `url` parameter of the `script.js`
- Setup [AWS CLI](https://aws.amazon.com/cli/) with your access credentials.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.