class Contribute:

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "coin_the_cat"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                *self._get_contribute_block()
            ],
        }

    def _get_contribute_block(self):
        text = (
            f"*Want to contribute to this Slack bot?*\n"
            "You can find the repository here: https://github.com/sydneyq/Coin-the-Cat\n"
            "Clone the repository and make a pull request or ask to become a Collaborator!"
        )
        information = (
            ":information_source: *<https://github.com/slackapi/python-slackclient/tree/main/tutorial|"
            "Take a look at the tutorial on how to develop a Slack bot>*"
        )
        return self._get_task_block(text, information)

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]
