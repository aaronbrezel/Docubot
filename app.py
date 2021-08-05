from flask import Flask, request
from utils.slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
from utils.slackUtils import receive_message, receive_reaction
from utils.db import setup_db
setup_db()

load_dotenv()
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

# This `app` represents your existing Flask app
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/events", app)

# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on('message')
def message(event, req):
    # ignore retries
    if req.headers.get('X-Slack-Retry-Reason'):
        print("Ignoring Retry")
        return "Status: OK"
    receive_message(event['event'])

@slack_events_adapter.on("reaction_added")
def reaction_added(event, req):
    # ignore retries
    if req.headers.get('X-Slack-Retry-Reason'):
        print("Ignoring Retry")
        return "Status: OK"
    receive_reaction(event['event'])

@app.route('/')
def index():
  return "<p>Hello, World!</p>"

@app.route('/', methods=['POST'])
def challenge():
  type = request.json.get('type', None)
  challenge_code = request.json.get('challenge', None)
  if challenge_code:
    return challenge_code
  if type:
    event = request.json.get('event', None)
    if event == "message":
      receive_message(event)
    if event == "reaction_added":
      reaction_added(event)
  return "bruh"



port = os.getenv("PORT")
if not port:
    port = 3000

# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=port)
