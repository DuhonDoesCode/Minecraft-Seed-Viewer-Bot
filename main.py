import discord
from discord.ext import commands
from selenium.webdriver.common.keys import Keys
from typing import Literal, Optional
from discord.ext.commands import Greedy, Context
from selenium import webdriver
import base64
import time
from selenium.webdriver.common.action_chains import ActionChains

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Bot()

# Tree syncer
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

driver = webdriver.Firefox()

@bot.tree.command()
async def view(interaction: discord.Interaction, seed: str, zoom: int):
    await interaction.response.send_message("Wait a bit while I fetch the map! (might take a few seconds)", ephemeral=True)
    driver.get("https://www.chunkbase.com/apps/seed-map#" + seed)
    canvas = driver.find_element("css selector", "canvas")
    print("found canvas")
    slider = driver.find_element("css selector", "#map-zoom-slider")
    print('found slider')
    if zoom > 500:
        zoom = 500
    elif zoom < -500:
        zoom = -500
    ActionChains(driver).click_and_hold(slider).move_by_offset(zoom, 0).release().perform()
    time.sleep(5)
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    canvas_png = base64.b64decode(canvas_base64)
    with open("canvas.png", 'wb') as f:
        f.write(canvas_png)
        f.close()
    print('saved canvas')
    await interaction.followup.send(file=discord.File("canvas.png"))

bot.run('MTA1Mjc0NDkwOTg4ODY5MjI5Ng.GfWEv7.QLE1nKA3tH3gnGN5W32A86Dn0sWrtRrlCf1L38')