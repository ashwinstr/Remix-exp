import goslate
import emoji
from emoji import get_emoji_regexp
from userbot.events import register


@register(outgoing=True, pattern="^.gs(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        # https://t.me/c/1220993104/192075
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.edit("`.gs LanguageCode` as reply to a message")
        return
    roman_gs = goslate.Goslate(writing=goslate.WRITING_ROMAN)
    text = emoji.demojize(text.strip())
    lan = lan.strip()
#    script = roman_gs.translate(text, lan) 
    try:
        scripted = goslate.Goslate(text, dest=lan)
        after_gs_text = scripted.text
        mono_gs_text = (("`{}`").format(after_gs_text))
        # TODO: emojify the :
        # either here, or before translation
        output_str = """**ROMANISED** from {} to {}
{}""".format(
            scripted.src,
            lan,
            mono_gs_text
        )
        
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))

