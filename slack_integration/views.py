from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Load Slack credentials from environment variables for better security
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")

# Function to send a message to a Slack channel
def send_slack_message(channel, message):
    client = WebClient(token=SLACK_BOT_TOKEN)    
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        return response
    except SlackApiError as e:
        # Log the error for debugging purposes
        print(f"Error sending message: {e.response['error']}")
        return None  # Return None to indicate failure
