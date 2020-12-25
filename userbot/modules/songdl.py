from telethon import events
import asyncio
from userbot.events import register
from userbot import bot, CMD_HELP, GOOGLE_CHROME_BIN, TEMP_DOWNLOAD_DIRECTORY, bot
from telethon.errors.rpcerrorlist import YouBlockedUserError
import os
import time
from asyncio.exceptions import TimeoutError
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo


@register(outgoing=True, pattern="^.sdl(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@songdl_bot"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
          await asyncio.sleep(2)
          await event.edit("`Downloading music taking some times,  Stay Tuned.....`")
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=635229672))
              await bot.send_message(chat, link)
              respond = await response
          except YouBlockedUserError:
              await event.reply("```Please unblock @SpotifyMusicDownloaderBot and try again```")
              return
          await event.delete()
          await bot.forward_messages(event.chat_id, respond.message)
