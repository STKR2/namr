from AarohiX import app
from typing import Union
from pyrogram.types import InlineKeyboardButton
from config import SUPPORT_CHANNEL, SUPPORT_CHAT, OWNER_ID


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
            InlineKeyboardButton(text=_["S_B_2"], callback_data="settings_helper"),
        ],
    ]
    if SUPPORT_CHANNEL:
        print(f"SUPPORT_CHANNEL: {SUPPORT_CHANNEL}")  # للتحقق من قيمة SUPPORT_CHANNEL
        buttons.append([InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}")])
    if SUPPORT_CHAT:
        print(f"SUPPORT_CHAT: {SUPPORT_CHAT}")  # للتحقق من قيمة SUPPORT_CHAT
        buttons.append([InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}")])
    return buttons


def private_panel(_, OWNER_ID: Union[bool, int] = None):
    buttons = [[InlineKeyboardButton(text=_["S_B_8"], callback_data="settings_back_helper")]]
    if SUPPORT_CHANNEL:
        print(f"SUPPORT_CHANNEL: {SUPPORT_CHANNEL}")  # للتحقق من قيمة SUPPORT_CHANNEL
        buttons.append([InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}")])
    if SUPPORT_CHAT:
        print(f"SUPPORT_CHAT: {SUPPORT_CHAT}")  # للتحقق من قيمة SUPPORT_CHAT
        buttons.append([InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}")])
    buttons.append(
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ]
    )
    if OWNER_ID:
        print(f"OWNER_ID: {OWNER_ID}")  # للتحقق من قيمة OWNER_ID
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_7"], user_id=OWNER_ID),
                InlineKeyboardButton(text=_["S_B_6"], url=f"https://t.me/{OWNER_ID}"),
            ]
        )
    buttons.append([InlineKeyboardButton(text=_["ST_B_6"], callback_data="LG")])
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="- اضفني .", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}"),
        ],
    ]
    return buttons
