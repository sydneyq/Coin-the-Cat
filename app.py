import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from contribute import Contribute
import resources
import json

# Initialize a Flask app to host the events adapter
from slack.errors import SlackApiError

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
client = slack_web_client

with open('data/resources.json') as f:
    resources_json = json.load(f)


def write_json(data, filename='data/resources.json'):
    with open(filename, 'w') as f_:
        json.dump(data, f, indent=4)


def contribute(user_id: str, channel: str):
    # Create a new onboarding tutorial.
    contribute_msg = Contribute(channel)

    # Get the onboarding message payload
    message = contribute_msg.get_message_payload()

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    thread_ts = event.get("ts")

    if text.startswith('!'):
        alises_cmds = ['cmd', 'cmds', 'commands', 'help']
        alises_links = ['links', 'link', 'resources']
        aliases_newlink = ['createlink', 'newlink', 'makelink', 'newresource', 'al', 'addlink']
        aliases_removelink = ['removelink', 'rl', 'deletelink', 'removeresource']

        # getting command & its args
        cmds = text[1:].lower()
        cmds = cmds.split()
        cmd = cmds[0]

        if cmd == 'contribute':
            # contribute msg
            return contribute(user_id, channel_id)
        elif cmd in alises_cmds:
            # print all available bot commands
            pass
        elif cmd in resources_json:
            # prints a specific link
            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=resources_json[cmd],
                    thread_ts=thread_ts
                )
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        elif cmd in alises_links:
            # prints all links
            text = ''

            try:
                for item in resources_json:
                    text += f'> *{item}*: {resources_json[item]}\n'
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=text,
                    thread_ts=thread_ts
                )
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        elif cmd in aliases_newlink:
            # enable people to be able to add links through an `!al [title] [link]` command
            resources_json[cmds[1]] = cmds[2]
            y = f'{cmds[1]}:{cmds[2]}'
            temp.append(y)
            write_json(resources_json)
            pass
        elif cmd in aliases_removelink:
            # enable people to delete links in the json through `!rl [title] [link]` command
            pass


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)

"""
# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack_events_adapter.on("reaction_added")
def update_emoji(payload):

    event = payload.get("event", {})

    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")

    if channel_id not in onboarding_tutorials_sent:
        return

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = slack_web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]
"""
