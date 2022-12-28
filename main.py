import argparse
import json
import pathlib
import re
from typing import Dict, TYPE_CHECKING

import discord
from discord.ext import commands
import gradio as gr
from gradio import utils
import requests


intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot("", intents=intents)
bot.guild_spaces = {}  # type: ignore
guild_spaces: Dict[int, gr.Blocks] = bot.guild_spaces  # type: ignore


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Running in {len(bot.guilds)} servers...")


async def send_file_or_text(channel, file_or_text: str):
    # if the file exists, send as a file
    if pathlib.Path(str(file_or_text)).exists():
        with open(file_or_text, "rb") as f:
            return await channel.send(file=discord.File(f))
    else:
        return await channel.send(file_or_text)


async def run_prediction(space: gr.Blocks, *inputs):
    inputs = list(inputs)
    fn_index = 0
    processed_inputs = space.serialize_data(fn_index=fn_index, inputs=inputs)
    batch = space.dependencies[fn_index]["batch"]

    if batch:
        processed_inputs = [[inp] for inp in processed_inputs]

    outputs = await space.process_api(
        fn_index=fn_index, inputs=processed_inputs, request=None, state={}
    )
    outputs = outputs["data"]

    if batch:
        outputs = [out[0] for out in outputs]

    processed_outputs = space.deserialize_data(fn_index, outputs)
    processed_outputs = utils.resolve_singleton(processed_outputs)

    return processed_outputs


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    else:
        if message.content:
            content = message.content.replace("<@1040198143695933501>", "").strip()
            guild = message.channel.guild
            assert guild, "Message not sent in a guild."

            if content == "exit":
                guild_spaces.pop(guild.id, None)
                await guild.me.edit(nick="GradioBot")
            elif content.startswith('"') or content.startswith("'"):
                if guild.id in guild_spaces:
                    params = re.split(r' (?=")', content)
                    params = [p.strip("'\"") for p in params]
                    space = guild_spaces[guild.id]
                    predictions = await run_prediction(space, *params)
                    if isinstance(predictions, (tuple, list)):
                        for p in predictions:
                            await send_file_or_text(message.channel, p)
                    else:
                        await send_file_or_text(message.channel, predictions)
                    return
                else:
                    await message.channel.send(
                        "No Space is currently running. Please type in the name of a Hugging Face Space name first, e.g. abidlabs/en2fr"
                    )
                    await guild.me.edit(nick="GradioBot")
            else:
                iframe_url = (
                    requests.get(f"https://huggingface.co/api/spaces/{content}/host")
                    .json()
                    .get("host")
                )
                if iframe_url is None:
                    return await message.channel.send(
                        f"Space: {content} not found. If you'd like to make a prediction, enclose the inputs in quotation marks."
                    )
                else:
                    await message.channel.send(
                        f"Loading Space: https://huggingface.co/spaces/{content}..."
                    )
                interface = gr.Interface.load(content, src="spaces")
                guild_spaces[guild.id] = interface
                if len(content) > 32 - len("GradioBot []"):
                    nickname = content[: 32 - len("GradioBot []") - 3] + "..."
                else:
                    nickname = content
                nickname = f"GradioBot [{nickname}]"
                await guild.me.edit(nick=nickname)
                await message.channel.send(
                    "Ready to make predictions! Type in your inputs and enclose them in quotation marks."
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "token",
        type=str,
        help="API key for the Discord bot. You can set this to your Discord token if you'd like to make your own clone of the Gradio Bot.",
        default="",
    )
    args = parser.parse_args()

    if args.token.strip():
        discord_token = args.token
    else:
        with open("secrets.json") as fp:
            discord_token = json.load(fp)["discord_token"]

    bot.run(discord_token)
