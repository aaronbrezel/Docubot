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

@app.route('/')
def index():
  return "<p>Hello, World!</p>"

@app.route('/', methods=['POST'])
def challenge():
  print(request.json)
  event = request.json.get('event')
  challenge_code = request.json.get('challenge')
  if challenge_code:
    return challenge_code
  if event:
    type = event.get('type')
    if type == "message":
      receive_message(event)
    if type == "reaction_added":     
      receive_reaction(event)
  return "bruh"



port = os.getenv("PORT")
if not port:
    port = 3000

# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=port)
