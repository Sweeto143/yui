import html
import json
import time
from datetime import datetime
from typing import Optional, List
from hurry.filesize import size as sizee

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, LOGGER
from tg_bot.__main__ import GDPR
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from requests import get

# DO NOT DELETE THIS, PLEASE.
# Made by @peaktogoo on GitHub and Telegram.
# This module was inspired by Android Helper Bot by Vachounet.
# None of the code is taken from the bot itself, to avoid any more confusion.

LOGGER.info("Original Android Modules by @peaktogoo on Telegram, modified by @HitaloSama on Telegram")
GITHUB = 'https://github.com'

@run_async
def magisk(bot, update):
    url = 'https://raw.githubusercontent.com/topjohnwu/magisk_files/'
    releases = ""
    for type, branch in {"Stable":["master/stable","master"], "Beta":["master/beta","master"], "Canary (release)":["canary/release","canary"], "Canary (debug)":["canary/debug","canary"]}.items():
        data = get(url + branch[0] + '.json').json()
        releases += f'*{type}*: \n' \
                    f'• [Changelog](https://github.com/topjohnwu/magisk_files/blob/{branch[1]}/notes.md)\n' \
                    f'• Zip - [{data["magisk"]["version"]}-{data["magisk"]["versionCode"]}]({data["magisk"]["link"]}) \n' \
                    f'• App - [{data["app"]["version"]}-{data["app"]["versionCode"]}]({data["app"]["link"]}) \n' \
                    f'• Uninstaller - [{data["magisk"]["version"]}-{data["magisk"]["versionCode"]}]({data["uninstaller"]["link"]})\n\n'

    update.message.reply_text("*Latest Magisk Releases:*\n{}".format(releases),
                              parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def superior(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/superior '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/superior whyred`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/SuperiorOS/official_devices/ten/builds/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = (f"• *Package Name:* `{filename}`\n"
                      f"• *Build size:* `{buildsize_b}`\n"
                      f"• *Version:* `{version}`")

        keyboard = [[InlineKeyboardButton(text="Click Here to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text = "Device not found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def miui(bot: Bot, update: Update):
    giturl = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/"
    message = update.effective_message
    device = message.text[len('/miui '):]
    result = "*Recovery ROM*\n\n"
    result += "*Stable*\n"
    stable_all = json.loads(get(giturl + "stable_recovery/stable_recovery.json").content)
    data = [i for i in stable_all if device == i['codename']]
    if len(data) != 0:
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")\n\n"

        result += "*Weekly*\n"
        weekly_all = json.loads(get(giturl + "weekly_recovery/weekly_recovery.json").content)
        data = [i for i in weekly_all if device == i['codename']]
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")"
    else:
        result = "Couldn't find any device matching your query."

    message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


__help__ = """
 - /superior <device>: Get the Superior OS Rom
 - /miui <stable/weekly>: Get the weekly or Stable Firmwares
 - /magisk: Get the latest magisk release for Stable/Beta/Canary.
"""

__mod_name__ = "Roms"


MIUI_HANDLER = DisableAbleCommandHandler("miui", miui, admin_ok=True)
SUPERIOR_HANDLER = DisableAbleCommandHandler("superior", superior, admin_ok=True)
MAGISK_HANDLER = CommandHandler("magisk", magisk)

dispatcher.add_handler(MIUI_HANDLER)
dispatcher.add_handler(SUPERIOR_HANDLER)
dispatcher.add_handler(MAGISK_HANDLER)
