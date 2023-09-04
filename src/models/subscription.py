from dataclasses import dataclass


@dataclass
class Subscription:
    chat_id: int
    event_name: str
