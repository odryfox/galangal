from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class UserRequest:
    message: Optional[str]
    signal: Optional[str]
    data: dict


class IBot:

    def parse_request(self, request: Any) -> Tuple[UserRequest, str]:
        pass

    def send_response(self, response: Any, chat_id: str):
        pass

    def send_responses(self, responses: List[Any], chat_id: str):
        for response in responses:
            self.send_response(response, chat_id)
