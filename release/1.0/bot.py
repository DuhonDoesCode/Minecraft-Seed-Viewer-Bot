import discord
from discord.ext import commands
from typing import Literal, Optional
from discord.ext.commands import Greedy, Context
import os
import subprocess

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Bot()

versionList = ['UNDEF', 'B1.8','1.0',
    '1.1',
    '1.2',
    '1.3',
    '1.4',
    '1.5',
    '1.6',
    '1.7',
    '1.8',
    '1.9',
    '1.10',
    '1.11',
    '1.12',
    '1.13',
    '1.14',
    '1.15',
    '1.16.1',
    '1.16',
    '1.17',
    '1.18',
    '1.19.2',
    '1.19']

# Biome names linked with their ID in Cubiomes
biomeList = {
    'Desert': 2,
    'Swamp': 6,
    'Mushroom Island': 14,
    'Beach': 16,
    'Badlands': 37
}

structuresList = ['Feature', 
    'Desert Pyramid',
    'Jungle Temple',
    'Swamp Hut',
    'Igloo',
    'Village',
    'Ocean Ruin',
    'Shipwreck',
    'Monument',
    'Mansion',
    'Outpost',
    'Ruined Portal',
    'Ancient City',
    'Treasure',
    'Mineshaft']

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
    nonoVersions = ['1.18', '1.19'] # These are being rendered wrongly in MineMap for some reason.
    if version in nonoVersions:
        await interaction.followup.send(f"Sorry, this version is not currently supported as the Map renderer tends to be wrong about it. However, you can still search for structures! For visualization I recommend https://www.chunkbase.com/apps/seed-map#{seed}")
    os.system(f"java -jar \"MineMap.jar\" --screenshot --seed {seed} --version {version} --pos {coords} --size {size}")
    file = discord.File(f"{seed}.png")
    await interaction.followup.send(f"Here's the render of the seed {seed}", file=file)

# Finds you a specified structure at a certain pair of coords
@bot.tree.command()
async def structure(interaction: discord.Interaction, version: str, structure: str):
    await interaction.response.send_message("Wait a moment while I find the structure desired!")
    if version not in versionList:
        await interaction.followup.send("I only support versions from B1.8 to 1.19 in this feature!")
        return
    if structure not in structuresList:
        await interaction.followup.send("Make sure your structure is typed correctly! Options are: 'Desert Pyramid','Jungle Temple', 'Jungle Temple','Swamp Hut','Igloo','Village','Ocean Ruin','Shipwreck','Monument','Mansion','Outpost','Ruined Portal','Ancient City','Treasure','Mineshaft'")
        return
    subprocess.call(["a.out", str(structuresList.index(structure)), structure, str(versionList.index(version))])
    f = open("tmp.txt", "r")
    result = f.read()
    f.close()
    os.remove("tmp.txt")
    await interaction.followup.send(result)

@bot.tree.command()
async def stronghold(interaction: discord.Interaction, version: str, seed: str):
    await interaction.response.send_message("Wait a moment while I find the stronghold!")
    if version not in versionList:
        await interaction.followup.send("I only support versions from B1.8 to 1.19 in this feature!")
        return
    subprocess.call(["b.out", str(seed), str(versionList.index(version))])
    f = open("tmp.txt", "r")
    result = f.read()
    f.close()
    os.remove("tmp.txt")
    await interaction.followup.send(result)

@bot.tree.command()
async def biome(interaction: discord.Interaction, version: str, biome: str, structure: str=None):
    await interaction.response.send_message("Looking for a seed with the biome at spawn! One moment")
    if structure not in structuresList:
        await interaction.followup.send("Make sure your structure is typed correctly! Options are: 'Desert Pyramid','Jungle Temple', 'Jungle Temple','Swamp Hut','Igloo','Village','Ocean Ruin','Shipwreck','Monument','Mansion','Outpost','Ruined Portal','Ancient City','Treasure','Mineshaft'")
    if version not in versionList:
        await interaction.followup.send("I only support versions from B1.8 to 1.19 in this feature!")
    if structure != None:
        subprocess.call(["d.out", str(biomeList[biome]), biome, str(versionList.index(version)), str(structuresList.index(structure))])
    else:
        subprocess.call(["c.out", str(biomeList[biome]), biome, str(versionList.index(version))])
        print("No structure specified.")
    if biome not in biomeList.keys():
        await interaction.followup.send("Sorry, the biome picked is not currently supported.")
        return   
    f = open("tmp.txt", "r")
    result = f.read()
    f.close()
    os.remove("tmp.txt")
    await interaction.followup.send(result)

@bot.tree.command()
async def search(interaction: discord.Interaction, version: str, seed: str, structure: str):
    await interaction.response.send_message("Looking for the structure! Wait a bit.")
    if structure not in structuresList:
        await interaction.followup.send("Make sure your structure is typed correctly! Options are: 'Desert Pyramid','Jungle Temple', 'Jungle Temple','Swamp Hut','Igloo','Village','Ocean Ruin','Shipwreck','Monument','Mansion','Outpost','Ruined Portal','Ancient City','Treasure','Mineshaft'")
    if version not in versionList:
        await interaction.followup.send("I only support versions from B1.8 to 1.19 in this feature!")
    subprocess.call(["e.out", str(seed), str(versionList.index(version)), str(structuresList.index(structure)), structure])
    f = open("tmp.txt", "r")
    result = f.read()
    f.close()
    os.remove("tmp.txt")
    await interaction.followup.send(result)
    

@bot.tree.command()
async def faq(interaction: discord.Interaction):
    await interaction.response.send_message("Thank you for using my bot! Map rendering tech provided by https://github.com/hube12/Minemap. Finders provided by https://github.com/Cubitect/cubiomes. Discord bot implementation made by Duhon.\nHelp server: https://discord.gg/ZBpgKVxVTR \nHow it works: It uses MineMap to render a picture and then send it on Discord. As simple as it gets. \nHow to use it: Use a slash command '/view'. The inputs should be a number seed for 'seed', the size of the render in 'size' (700+ recommended), 'version' in the form 'X.XX' (1.18 and up not currently supported), and 2 whole numbers 'X Z' in 'coords'. All other commands follow the same patterns here/teach you how to use them when they fail.")

bot.run('your_token')