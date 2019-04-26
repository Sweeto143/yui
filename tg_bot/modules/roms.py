import subprocess
import html
import json
import random
import time
import pyowm
from pyowm import timeutils, exceptions
from datetime import datetime
from typing import Optional, List
from hurry.filesize import size

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER
from tg_bot.__main__ import GDPR
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from requests import get

# DO NOT DELETE THIS PLEASE
# Worked by @peaktogo on github and telegram
# This module was inspired by Android Helper Bot by Vachounet
# None of the code were taken from the bot, to avoid any more confusion.

print("Original Android Modules by @peaktogoo on Telegram")

@run_async
def pixys(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/pixys '):]
    fetch = get(f'https://raw.githubusercontent.com/PixysOS-Devices/official_devices/master/{device}/build.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Rom Type:* `{usr['response'][0]['romtype']}`
*Version:* `{usr['response'][0]['version']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def superior(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/superior '):]
    fetch = get(f'https://raw.githubusercontent.com/SuperiorOS/official_devices/pie/{device}.json')
    if fetch.status_code == 200 and str(fetch.json()['response']) != "[]":
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][-1]['filename']}]({usr['response'][-1]['url']})
*Size:* `{usr['response'][-1]['size']}`
*Rom Type:* `{usr['response'][0]['romtype']}`
*Version:* `{usr['response'][-1]['version']}`
"""
    else:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def dot(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/dot '):]
    fetch = get(f'https://raw.githubusercontent.com/DotOS/ota_config/dot-p/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Version:* `{usr['response'][0]['version']}`
*Device Changelog:* `{usr['response'][0]['changelog_device']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def miui(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/miui '):]
    result = "*Recovery ROM*\n"
    result += "*Stable*\n"
    stable_all = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_recovery/stable_recovery.json").content)
    data = [i for i in stable_all if device == i['codename']]
    for i in data:
        result += "[" + i['filename'] + "](" + i['download'] + ")\n"

    result += "*Weekly*\n"
    weekly_all = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_recovery/weekly_recovery.json").content)
    data = [i for i in weekly_all if device == i['codename']]
    for i in data:
        result += "[" + i['filename'] + "](" + i['download'] + ")\n"

    message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


__help__ = """
 - /dot <device>: Get the DotOS Rom
 - /pixys <device>: Get the Pixys Rom
 - /superior <device>: Get the Superior OS Rom
 - /miui <stable/weekly>: Get the weekly or Stable Firmwares
"""

__mod_name__ = "Roms"


MIUI_HANDLER = DisableAbleCommandHandler("miui", miui, admin_ok=True)
DOTOS_HANDLER = DisableAbleCommandHandler("dot", dot, admin_ok=True)
PIXYS_HANDLER = DisableAbleCommandHandler("pixys", pixys, admin_ok=True)
SUPERIOR_HANDLER = DisableAbleCommandHandler("superior", superior, admin_ok=True)

dispatcher.add_handler(MIUI_HANDLER)
dispatcher.add_handler(DOTOS_HANDLER)
dispatcher.add_handler(PIXYS_HANDLER)
dispatcher.add_handler(SUPERIOR_HANDLER)
