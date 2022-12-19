import json
import pathlib
import re
from typing import Dict

import discord
from discord.ext import commands
import gradio as gr
import requests


with open("secrets.json") as fp:
    discord_token = json.load(fp)["discord_token"]

intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot("", intents=intents)
bot.guild_spaces: Dict[int, str] = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
 

async def send_file_or_text(channel, file_or_text):
    # if the file exists, send as a file
    if pathlib.Path(str(file_or_text)).exists():
        with open(file_or_text, "rb") as f:
            return await channel.send(file=discord.File(f))
    else:
        return await channel.send(file_or_text)
        
 
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    else:
        if message.content:
            content = message.content.replace("<@1040198143695933501>", "").strip()
            guild = message.channel.guild
            
            print(content)
            if content == "exit":
                bot.guild_spaces.pop(guild.id, None)
                await guild.me.edit(nick="GradioBot")
            elif content.startswith("\"") or content.startswith("\'"):
                if guild.id in bot.guild_spaces:
                    params = re.split(r' (?=")', content)
                    params = [p.strip("\'\"") for p in params]
                    print(params)
                    interface = bot.guild_spaces[guild.id]
                    predictions = interface(*params)
                    if isinstance(predictions, (tuple, list)):
                        for p in predictions:
                            await send_file_or_text(message.channel, p)
                    else:
                        await send_file_or_text(message.channel, predictions)
                    return
                else:
                    await message.channel.send("No Space is currently running. Please type in the name of a Hugging Face Space name first, e.g. abidlabs/en2fr")
                    await guild.me.edit(nick="GradioBot")                    
            else:
                iframe_url = (
                    requests.get(f"https://huggingface.co/api/spaces/{content}/host")
                    .json()
                    .get("host")
                )                
                if iframe_url is None:
                    return await message.channel.send(f"Space: {content} not found. If you'd like to make a prediction, enclose the inputs in quotation marks.")
                else:
                    await message.channel.send(f"Loading Space: https://huggingface.co/spaces/{content}...")
                interface = gr.Interface.load(content, src="spaces")
                bot.guild_spaces[guild.id] = interface
                if len(content) > 32 - len("GradioBot []"):
                    nickname = content[:32 - len("GradioBot []") - 3] + "..."
                else:
                    nickname = content
                nickname = f"GradioBot [{nickname}]"
                await guild.me.edit(nick=nickname)
                await message.channel.send("Ready to make predictions! Type in your inputs and enclose them in quotation marks.")
                    
bot.run(discord_token)
