import asyncio
import json
import pathlib
from typing import Dict

import discord

lock = asyncio.Lock()


async def update_guild_spaces_file(guild_spaces: Dict, file_path: str):
    async with lock:
        with open(file_path, "w") as fp:
            json.dump(guild_spaces, fp)


async def send_file_or_text(channel, file_or_text: str):
    # if the file exists, send as a file
    if pathlib.Path(str(file_or_text)).exists():
        with open(file_or_text, "rb") as f:
            return await channel.send(file=discord.File(f))
    else:
        return await channel.send(file_or_text)


def remove_tags(content: str) -> str:
    content = content.replace("<@1040198143695933501>", "")
    content = content.replace("<@1057338428938788884>", "")
    return content.strip()
    