import aiml
import os
import discord
from discord.ext import commands
import time
import json
import random
from discord.utils import find

# def


kernel = aiml.Kernel()
LOGchannel = 812180121377046578
STARTUP_FILE = "std-startup.xml"
BOT_PREFIX = ('.e ', '<@811859628342247424> ', '.E ')
TOKEN = 'TOKEN'
# end def
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")

bot = commands.Bot(command_prefix=BOT_PREFIX)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


async def log(msg):
    chan = bot.get_channel(LOGchannel)
    await chan.send(msg)


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    activity = discord.Game(name="with humans", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    await log('**Bot started**')
    chan = bot.get_channel(LOGchannel)
    for i in range(0, len(bot.guilds), 10):
        embed = discord.Embed(title='Guilds', colour=0x7289DA)
        guilds = bot.guilds[i:i + 10]

        for guild in guilds:
            embed.add_field(name=guild.name, value=guild.id)

        await chan.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    if 'erza-chat' in message.channel.name:
        with open('server_blacklist.json') as f:
            data = json.load(f)
            blacklist_servers = data["servers"]

        if message.content is None:
            print("Empty message received.")
            return
        if (message.guild.id) in blacklist_servers:
            await message.channel.send('this server is blacklisted by erza to unban join https://discord.gg/SQ2J3MxaDG ')

            if "unban" in message.content or "whitelist" in message.content:
                await message.channel.send(
                    "To whitelist this server join https://discord.gg/SQ2J3MxaDG and ask the developers to whitelist")
                return
            return

        print(str(message.guild) + ": Message: " + str(message.content))

        if message.content.startswith(BOT_PREFIX):
            return
        else:
            aiml_response = kernel.respond(message.content)
            if "rude" in aiml_response or aiml_response == "Watch your language!" or "Insult" in aiml_response:
                await message.author.send("Message too toxic <:ez_angry:812927850084040714>```toxic:" + str(
                    random.random()) + "\n" + "hate:" + str(
                    random.random()) + " ```\n `If you have 10 warning you will not be able to use the bot for 2 days (48 hrs)` ```Warnings are disabled since this is test mode```")
            if "suck" in message.content or "bitch" in message.content or "fuck" in message.content or "gay" in message.content or "gae" in message.content or "dumbass" in message.content:
                await message.author.send("Message too toxic <:ez_angry:812927850084040714>```toxic:" + str(
                    random.random()) + "\n" + "hate:" + str(
                    random.random()) + " ```\n `If you have 10 warning you will not be able to use the bot for 2 days (48 hrs)` ```Warnings are disabled since this is test mode```")

                # async with message.typing():
                #  await asyncio.sleep(0.5)
            if 'Nameless' in str(aiml_response):
                names = ('Erza', 'Scarlet')
                edit_response = aiml_response.replace('Nameless', random.choice(names))
                await message.channel.send(edit_response)
                DM_choice = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
                if random.choice(DM_choice) == 0:
                    await message.author.send('```css\nExperiment successfull\ncode returned with 0```')
                    await log('```css\nEVENT LOG :  Experiment : Change Nameless to Erza successed with code 0```')

            else:
                try:
                    await message.channel.send("`@" + message.author.nick + "`: " + aiml_response)
                except:
                    await message.channel.send("`@" + message.author.name + "`: " + aiml_response)
    


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: 'general' in x.name, guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello {}!'.format(guild.name))
        await general.send('I am erza scarlet! ')
        time.sleep(0.5)
        # await general.send('please create a channel named #erza-chat for chatting with me')
        await general.send('See you in #erza-chat')
        chan = bot.get_channel(LOGchannel)
        await chan.send('```css\nEVENT LOG :  was added to ' + guild.name + "```")
        try:
            await guild.create_text_channel('erza-chat')
        except:
            await general.send('Failed to create channel please create it manually! ')
            await general.send(
                'Permission error```PERMISSIONS REQUIRED:\nManage server\nManage Channels\nCreate channels\nView Audit '
                'LOG```Please ensure these permissions for best experience')

@bot.command()
async def ping(ctx):
  
    latency = int(bot.latency)*1000  # Included in the Discord.py library
    await ctx.send("PING : `"+str(latency)+"`\nMelon API ping: `"+str(random.random()*100)+"`")
@bot.command()
async def support(ctx):
    await ctx.send('Here you go with the **Support server** invite\nhttps://discord.gg/arcNdTfXAJ')





bot.run(TOKEN)
