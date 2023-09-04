from abc import ABC, abstractmethod
from src.models import Subscription


class ISubscriptionRepo(ABC):
    @abstractmethod
    async def save(self, sub: Subscription) -> None:
        pass

    @abstractmethod
    async def get_chats_by_sub_name(self, sub: str) -> list[int]:
        pass

    @abstractmethod
    async def delete_subs_by_chat_id(self, chat_id: int) -> None:
        pass
