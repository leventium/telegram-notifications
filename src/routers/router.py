import re
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from src.plugin_manager import PluginManager
from src.config import PASSWORD
from src.database import ISubscriptionRepo
from src.models import Subscription
from src.logger import logger

router = Router()
subscription_string_splitter = re.compile(r" |,")


class ChatProgress(StatesGroup):
    auth = State()
    subscriptions = State()
    waiting = State()


def get_notice_suggestion_msg() -> str:
    events = PluginManager().get_events_names()
    msg = "*Available events:*\n"
    for i, name in enumerate(events):
        msg += f"{i + 1}. {name}\n"
    msg += (
        "\nWrite down the numbers of the events you want to "
        "subscribe to (comma or space separated):"
    )
    return msg


def parce_subscription_numbers(msg: str) -> list[int]:
    list_with_gaps = list(map(int, subscription_string_splitter.split(msg)))
    return [elem for elem in list_with_gaps if elem != ""]


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if PASSWORD != "":
        await state.set_state(ChatProgress.auth)
        await message.answer(
            "Password?",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await state.set_state(ChatProgress.subscriptions)
    await message.answer(
        get_notice_suggestion_msg(),
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ChatProgress.auth)
async def authentication(message: Message, state: FSMContext) -> None:
    if message.text == PASSWORD:
        await state.set_state(ChatProgress.subscriptions)
        await message.answer("Nice")
        await message.answer(get_notice_suggestion_msg())
        logger.info(f"Chat - {message.chat.id} - authorized")
        return


@router.message(ChatProgress.subscriptions)
async def subscribe(
        message: Message,
        state: FSMContext,
        sub_repo: ISubscriptionRepo
) -> None:
    try:
        items_to_subscribe = parce_subscription_numbers(message.text)
        logger.debug(f"Numbers to subscribe: {items_to_subscribe}")
    except ValueError:
        await message.answer("Invalid request. Try again")
        return

    try:
        events = PluginManager().get_events_names()
        subscriptions = [
            Subscription(message.chat.id, events[sub_number-1])
            for sub_number in items_to_subscribe
        ]
    except IndexError:
        await message.answer("Number is out of given range. Try again")
        return

    for sub in subscriptions:
        await sub_repo.save(sub)

    await state.set_state(ChatProgress.waiting)
    await message.answer("Ok. I've got it. Wait for notifications")
    await message.answer(
        "Also. Send \"Update Subscriptions\" to delete "
        "current subscriptions and subscribe again",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Update Subscriptions")]],
            resize_keyboard=True
        )
    )
    logger.info(
        f"Chat - {message.chat.id} - "
        f"subscribed on {items_to_subscribe}"
    )


@router.message(
    ChatProgress.waiting,
    F.text.casefold() == "update subscriptions"
)
async def update_subscriptions(
        message: Message,
        state: FSMContext,
        sub_repo: ISubscriptionRepo
) -> None:
    await sub_repo.delete_subs_by_chat_id(message.chat.id)
    await state.set_state(ChatProgress.subscriptions)
    await message.answer(
        get_notice_suggestion_msg(),
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info(f"Chat - {message.chat.id} - cleared subscriptions")
