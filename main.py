import asyncio
import argparse
import json
import pathlib
import re


import discord
from discord.ext import commands
import gradio as gr
from gradio import utils
import requests


from utils import *


lock = asyncio.Lock()

bot = commands.Bot("", intents=discord.Intents(messages=True, guilds=True))


GUILD_SPACES_FILE = "guild_spaces.json"

if pathlib.Path(GUILD_SPACES_FILE).exists():
    with open(GUILD_SPACES_FILE) as fp:
        guild_spaces = json.load(fp)
        assert isinstance(guild_spaces, dict), "guild_spaces.json in invalid format."
else:
    guild_spaces = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Running in {len(bot.guilds)} servers...")


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


async def display_stats(message: discord.Message):
    await message.channel.send(f"Running in {len(bot.guilds)} servers...")


async def load_space(guild: discord.Guild, message: discord.Message, content: str):
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
    guild_spaces[guild.id] = interface  # type: ignore
    asyncio.create_task(update_guild_spaces_file(guild_spaces))
    if len(content) > 32 - len(f"{bot.name} []"):  # type: ignore
        nickname = content[: 32 - len(f"{bot.name} []") - 3] + "..."  # type: ignore
    else:
        nickname = content
    nickname = f"{bot.name} [{nickname}]"  # type: ignore
    await guild.me.edit(nick=nickname)
    await message.channel.send(
        "Ready to make predictions! Type in your inputs and enclose them in quotation marks."
    )


async def disconnect_space(bot: commands.Bot, guild: discord.Guild):
    guild_spaces.pop(guild.id, None)
    asyncio.create_task(update_guild_spaces_file(guild_spaces))
    await guild.me.edit(nick=bot.name)  # type: ignore


async def make_prediction(guild: discord.Guild, message: discord.Message, content: str):
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
        await guild.me.edit(nick=bot.name)  # type: ignore


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    else:
        if message.content:
            content = message.content.replace("<@1040198143695933501>", "").strip()
            content = message.content.replace("<@1057338428938788884>", "").strip()

            guild = message.channel.guild
            assert guild, "Message not sent in a guild."

            if content.strip() == "exit":
                await disconnect_space(bot, guild)
            elif content.strip() == "stats":
                await display_stats(message)
            elif content.startswith('"') or content.startswith("'"):
                await make_prediction(guild, message, content)
            else:
                await load_space(guild, message, content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token",
        type=str,
        help="API key for the Discord bot. You can set this to your Discord token if you'd like to make your own clone of the Gradio Bot.",
        required=False,
        default="",
    )
    args = parser.parse_args()

    if args.token.strip():
        discord_token = args.token
        bot.env = "staging"  # type: ignore
        bot.name = "StagingBot"  # type: ignore
    else:
        with open("secrets.json") as fp:
            discord_token = json.load(fp)["discord_token"]
        bot.env = "prod"  # type: ignore
        bot.name = "GradioBot"  # type: ignore

    bot.run(discord_token)
