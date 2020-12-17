# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import random
from urllib.parse import quote_plus

import aiofiles
from selenium import webdriver
from userbot.events import register
from userbot import GOOGLE_CHROME_BIN, DOWN_PATH, bot

CARBON = "https://carbon.now.sh/?t={theme}&l={lang}&code={code}&bg={bg}"


@register(outgoing=True, pattern="^.karbon2")
async def carbon(msg):
    replied = msg.reply_to_message
    if GOOGLE_CHROME_BIN is None:
        text = replied.text if replied else msg.text
        if not text:
            await msg.err("need input text!")
            return
        await msg.edit("`Creating a Carbon...`")
        try:
            await msg.send_message(text)
        await msg.click(x=random.randint(0, 2), y=random.randint(0, 8))
        caption = "\n".join(response.caption.split("\n")[0:2])
        file_id = msg.document.file_id
        await asyncio.gather(
            msg.delete(),
            msg.client.send_document(
                chat_id=msg.chat.id,
                document=file_id,
                caption="`" + caption + "`",
                reply_to_message_id=replied.message_id if replied else None,
            ),
        )
    else:
        input_str = msg.filtered_input_str
        theme = "seti"
        lang = "auto"
        red = msg.flags.get("r", random.randint(0, 255))
        green = msg.flags.get("g", random.randint(0, 255))
        blue = msg.flags.get("b", random.randint(0, 255))
        alpha = msg.flags.get("a", random.randint(0, 100))
        bg_ = f"rgba({red}, {green}, {blue}, {alpha})"
        if replied and (
            replied.text or (replied.document and "text" in replied.document.mime_type)
        ):
            message_id = replied.message_id
            if replied.document:
                await msg.edit("`Downloading File...`")
                path_ = await msg.client.download_media(
                    replied, file_name=Config.DOWN_PATH
                )
                async with aiofiles.open(path_) as file_:
                    code = await file_.read()
                os.remove(path_)
            else:
                code = replied.text
            if input_str:
                if "|" in input_str:
                    args = input_str.split("|")
                    if len(args) == 2:
                        theme = args[0].strip()
                        lang = args[1].strip()
                else:
                    theme = input_str
        elif input_str:
            message_id = msg.message_id
            if "|" in input_str:
                args = input_str.split("|")
                if len(args) == 3:
                    theme = args[0].strip()
                    lang = args[1].strip()
                    code = args[2].strip()
                elif len(args) == 2:
                    theme = args[0].strip()
                    code = args[1].strip()
            else:
                code = input_str
        else:
            await msg.err("need input text!")
            return
        await msg.edit("`Creating a Carbon...`")
        code = quote_plus(code)
        await msg.edit("`Processing... 20%`")
        carbon_path = os.path.join(DOWN_PATH, "carbon.png")
        if os.path.isfile(carbon_path):
            os.remove(carbon_path)
        url = CARBON.format(theme=theme, lang=lang, code=code, bg=bg_)
        if len(url) > 2590:
            await msg.err("input too large!")
            return
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        prefs = {"download.default_directory": Config.DOWN_PATH}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        await msg.edit("`Processing... 40%`")
        driver.command_executor._commands[
            "send_command"
        ] = (  # pylint: disable=protected-access
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": Config.DOWN_PATH},
        }
        driver.execute("send_command", params)
        # driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
        driver.find_element_by_id("export-menu").click()
        await asyncio.sleep(1)
        await msg.edit("`Processing... 60%`")
        driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
        await asyncio.sleep(1)
        driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
        await msg.edit("`Processing... 80%`")
        while not os.path.isfile(carbon_path):
            await asyncio.sleep(0.5)
        await msg.edit("`Processing... 100%`")
        await msg.edit("`Uploading Carbon...`")
        await asyncio.gather(
            msg.delete(),
            msg.client.send_photo(
                chat_id=msg.chat.id,
                photo=carbon_path,
                reply_to_message_id=message_id,
            ),
        )
        os.remove(carbon_path)
        driver.quit()

CMD_HELP.update(
    "karbon2",
    about={
        "header": "create a carbon",
        "flags": {
            "-r": "red -> 0-255",
            "-g": "green -> 0-255",
            "-b": "blue -> 0-255",
            "-a": "alpha -> 0-100",
        },
        "usage": "{tr}carbon [flags] [theme] | [language] | [text | reply to msg]",
        "examples": [
            "{tr}carbon haha",
            "{tr}carbon vscode | hoho",
            "{tr}carbon -r100 -g75 -b50 -a50 blackboard | hola",
        ],
        "themes": [
            "3024-night",
            "a11y-dark",
            "blackboard",
            "base16-dark",
            "base16-light",
            "cobalt",
            "dracula",
            "duotone-dark",
            "hopscotch",
            "lucario",
            "material",
            "monokai",
            "night-owl",
            "nord",
            "oceanic-next",
            "one-light",
            "one-dark",
            "panda-syntax",
            "paraiso-dark",
            "seti",
            "shades-of-purple",
            "solarized dark",
            "solarized light",
            "synthwave-84",
            "twilight",
            "verminal",
            "vscode",
            "yeti",
            "zenburn",
        ],
    },
    del_pre=True,
)
