from typing import Dict, Callable, Any

from py_netgames_model.messaging.message import Message, MatchRequestMessage, MatchStartedMessage, MoveMessage
from py_netgames_model.messaging.webhook_payload import WebhookPayload, WebhookPayloadType


class WebhookPayloadDeserializer:
    __deserialization_table: Dict[WebhookPayloadType, Callable[[Dict[str, Any]], Message]]

    def __init__(self):
        self.__deserialization_table = {
            WebhookPayloadType.MATCH_REQUEST: MatchRequestMessage.from_dict,
            WebhookPayloadType.MATCH_STARTED: MatchStartedMessage.from_dict,
            WebhookPayloadType.MOVE: MoveMessage.from_dict
        }

    def deserialize(self, message) -> Message:
        webhook_payload = WebhookPayload.from_json(message)
        return self.__deserialization_table[webhook_payload.type](webhook_payload.message)
