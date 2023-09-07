from src.models import Subscription
from .interfaces import ISubscriptionRepo
from src.logger import logger


class MemorySubscriptionRepo(ISubscriptionRepo):
    def __init__(self):
        self.storage: dict[str, set[int]] = dict()

    async def save(self, sub: Subscription) -> None:
        if sub.event_name not in self.storage:
            self.storage[sub.event_name] = set()
        self.storage[sub.event_name].add(sub.chat_id)
        logger.debug(self.storage)

    async def get_chats_by_sub_name(self, sub: str) -> list[int]:
        return list(self.storage.get(sub, set()))

    async def delete_subs_by_chat_id(self, chat_id: int) -> None:
        for event_ids in self.storage.values():
            event_ids.discard(chat_id)
        logger.debug(self.storage)
