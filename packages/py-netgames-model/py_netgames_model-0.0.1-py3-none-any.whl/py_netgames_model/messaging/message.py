import abc
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

from dataclasses_json import dataclass_json

from py_netgames_model.messaging.webhook_payload import WebhookPayloadType, WebhookPayload


@dataclass
class Message(ABC):

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abc.abstractmethod
    def type(self) -> WebhookPayloadType:
        raise NotImplementedError()

    def to_payload(self) -> WebhookPayload:
        return WebhookPayload(self.type(), self.to_dict())


@dataclass_json
@dataclass
class MatchRequestMessage(Message):
    game_id: UUID
    amount_of_players: int

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MATCH_REQUEST

    def to_dict(self) -> str:
        return MatchRequestMessage.to_dict(self)


@dataclass_json
@dataclass
class MatchStartedMessage(Message):
    match_id: UUID
    position: int

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MATCH_STARTED

    def to_dict(self) -> str:
        return MatchStartedMessage.to_dict(self)


@dataclass_json
@dataclass
class MoveMessage(Message):
    match_id: UUID
    payload: Dict[str, any]

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MOVE

    def to_dict(self) -> str:
        return MoveMessage.to_dict(self)
