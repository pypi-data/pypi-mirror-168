import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from hautils.logger import logger


def slack_notify(message):
    client = WebClient(token="xoxb-2344174290615-4076585965415-BxGLLtxcoGZEfZ1hORf1ek4I")
    try:
        response = client.chat_postMessage(channel='#engineering', text=message, mrkdwn=True)
        logger.warn("slack notification sent %s" % (response.status_code,))
    except SlackApiError as e:
        logger.error("error sending slack notification %s" % (e.response["error"]))
