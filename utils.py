async def update_guild_spaces_file(guild_spaces):
    async with lock:
        with open(GUILD_SPACES_FILE, "w") as fp:
            json.dump(guild_spaces, fp)


async def send_file_or_text(channel, file_or_text: str):
    # if the file exists, send as a file
    if pathlib.Path(str(file_or_text)).exists():
        with open(file_or_text, "rb") as f:
            return await channel.send(file=discord.File(f))
    else:
        return await channel.send(file_or_text)
