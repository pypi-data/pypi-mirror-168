from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from dataclasses_json import dataclass_json


class WebhookPayloadType(Enum):
    MATCH_REQUEST = 'MATCH_REQUEST'
    MATCH_STARTED = 'MATCH_STARTED'
    MOVE = 'MOVE'


@dataclass_json
@dataclass
class WebhookPayload:
    type: WebhookPayloadType
    message: Dict[str, Any]

    def to_json(self) -> str:
        return WebhookPayload.to_json(self)
