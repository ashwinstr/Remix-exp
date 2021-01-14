"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP, QUOTES_API_TOKEN

from userbot.events import register

def convert_tosticker(response, filename=None):
    filename = filename or os.path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    os.remove(response)
    return filename

def progress(
    current, total, gdrive, start, prog_type, file_name=None, is_cancelled=False
):
    now = time.time()
    diff = now - start
    if is_cancelled is True:
        raise CancelProcess

    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        eta = round((total - current) / speed)
        if "upload" in prog_type.lower():
            status = "Uploading"
        elif "download" in prog_type.lower():
            status = "Downloading"
        else:
            status = "Unknown"
        progress_str = "`{0}` | `[{1}{2}] {3}%`".format(
            status,
            "".join(["▰" for i in range(math.floor(percentage / 10))]),
            "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = (
            f"{progress_str}\n"
            f"`{humanbytes(current)} of {humanbytes(total)}"
            f" @ {humanbytes(speed)}`\n"
            f"**ETA :**` {time_formatter(eta)}`\n"
            f"**Duration :** `{time_formatter(elapsed_time)}`"
        )
        if file_name:
            gdrive.edit(
                f"**{prog_type}**\n\n"
                f"**File Name : **`{file_name}`**\nStatus**\n{tmp}"
            )
        else:
            gdrive.edit(f"**{prog_type}**\n\n" f"**Status**\n{tmp}")


@register(outgoing=True, pattern=r"^\.q")
async def stickerchat(quotes):
    if quotes.fwd_from:
        return
    reply = await quotes.get_reply_message()
    if not reply:
        await quotes.edit("`I cant quote the message. Reply to a message.`")
        return
    fetchmsg = reply.message
    repliedreply = None
    if reply.media and reply.media.document.mime_type in ("mp4"):
        await edit_or_reply(quotes, "`this format is not supported now`")
        return
    event = await quotes.edit("`Making quote...`")
    user = (
        await event.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    
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
