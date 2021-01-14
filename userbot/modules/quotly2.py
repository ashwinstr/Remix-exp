"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import process
from userbot.events import register

def convert_tosticker(response, filename=None):
    filename = filename or os.path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    os.remove(response)
    return filename

@register(outgoing=True, pattern=r"^\.q")
async def stickerchat(quotes):
    if quotes.fwd_from:
        return
    reply = await quotes.get_reply_message()
    if not reply:
        await edit_or_reply(
            catquotes, "`I cant quote the message. Reply to a message.`"
        )
        return
    fetchmsg = reply.message
    repliedreply = None
    if reply.media and reply.media.document.mime_type in ("mp4"):
        await edit_or_reply(quotes, "`this format is not supported now`")
        return
    event = await edit_or_reply(quotes, "`Making quote...`")
    user = (
        await event.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, catmsg = await process(fetchmsg, user, quotes.client, reply, repliedreply)
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    catmsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await quotes.client.send_file(quotes.chat_id, endfi, reply_to=reply)
    await event.delete()
    os.remove(endfi)



CMD_HELP.update(
    {
        "quotly": "**Plugin :** `quotly`\
        \n\n**  •Syntax : **`.q reply to messge`\
        \n**  •Function : **__Makes your message as sticker quote__\
        \n\n**  •Syntax : **`.qbot reply to messge`\
        \n**  •Function : **__Makes your message as sticker quote by @quotlybot__\
        "
    }
)
