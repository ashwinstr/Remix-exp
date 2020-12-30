from telethon.tl.types import User
from userbot import (LOGS, NC_LOG_P_M_S, PM_LOGGR_BOT_API_ID, bot)

from userbot.events import register


@register(incoming=True, outgoing=True, disable_edited=False)
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if event.is_private and not (await event.get_sender()).bot:
        chat = await event.get_chat()
        self_user = await event.client.get_me()
        if chat.id and chat.id != 777000:
            try:
                e = await event.client.get_entity(int(PM_LOGGR_BOT_API_ID))
                fwd_message = await event.client.forward_messages(
                    e,
                    event.message,
                    silent=True
                )
            except Exception as e:
                LOGS.warn(str(e))
                       
        if sender.id != self_user.id:
             return
        else:
            if event.chat_id and NC_LOG_P_M_S:
                await event.client.send_message(
                    PM_LOGGR_BOT_API_ID,
                    "#chat " + "[{chat.first_name}](tg://user?id={chat.id})",
                )
