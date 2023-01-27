import discord
from discord.ext import commands
from typing import Literal, Optional
from discord.ext.commands import Greedy, Context
import os

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

@bot.tree.command()
async def view(interaction: discord.Interaction, seed: str, size: int, version: str, coords: str):
    await interaction.response.send_message("Wait a bit while I render it!")
    os.system(f"java -jar \"PATH\TO\MINEMAP\JAR\" --screenshot --seed {seed} --version {version} --pos {coords} --size {size}")
    file = discord.File(f"{seed}.png")
    await interaction.followup.send(f"Here's the render of the seed {seed}", file=file)

@bot.tree.command()
async def faq(interaction: discord.Interaction):
    await interaction.response.send_message("Thank you for using my bot! Map rendering tech provided by https://github.com/hube12/Minemap. Discord bot implementation made by Duhon.\nHelp server: https://discord.gg/ZBpgKVxVTR \nHow it works: It uses MineMap to render a picture and then send it on Discord. As simple as it gets. \nHow to use it: Use a slash command '/view'. The inputs should be a number seed for 'seed', the size of the render in 'size' (700+ recommended), 'version' in the form 'X.XX', and 2 whole numbers 'X Z' in 'coords'.")

bot.run('your_token')