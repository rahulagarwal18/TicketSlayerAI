import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI
import requests
import json

# Load environment variables
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# We will use your main portfolio repo to test creating issues
GITHUB_REPO = "rahulagarwal18/rahulagarwal18" 

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize OpenAI client pointed at Groq's insanely fast free API
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    """
    Listens for any @TicketSlayer mentions in Slack.
    """
    event = body.get("event", {})
    text = event.get("text", "")
    user = event.get("user", "")
    
    # 1. Send an immediate acknowledgement
    say(f"Hold on <@{user}>, I'm analyzing that bug and turning it into a GitHub ticket...")
    
    try:
        # 2. Ask Groq (Llama-3) to extract the bug details and format them as JSON
        prompt = f"""
        You are an expert QA Engineer. A user just reported a bug in a Slack channel.
        Extract the problem and format it into a professional GitHub issue.
        Return ONLY a raw JSON object with exactly two keys: "title" and "body".
        No markdown formatting outside the JSON, no explanation, just the JSON string.
        
        Bug Report: {text}
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Strip any accidental markdown blocks that the LLM might have added
        if ai_response.startswith("```json"):
            ai_response = ai_response[7:-3]
            
        bug_data = json.loads(ai_response)
        
        # 3. Create the Issue via GitHub API
        github_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "title": f"[TicketSlayer] {bug_data['title']}",
            "body": f"{bug_data['body']}\n\n*Reported via Slack by <@{user}>*"
        }
        
        gh_res = requests.post(github_url, headers=headers, json=payload)
        
        if gh_res.status_code == 201:
            issue_url = gh_res.json().get("html_url")
            say(f"✅ **Ticket successfully created!**\nView the GitHub Issue here: {issue_url}")
        else:
            say(f"❌ I parsed the bug, but failed to create the GitHub Issue. Status: {gh_res.status_code}\n{gh_res.text}")
            
    except Exception as e:
        logger.error(f"Error processing mention: {e}")
        say(f"❌ Oops, something went wrong while processing that ticket: {str(e)}")

if __name__ == "__main__":
    print("[READY] TicketSlayer AI is running in Socket Mode! Waiting for messages...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
