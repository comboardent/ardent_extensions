import json
import random
import urllib

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

from utils import *


class NSFW():
    def __init__(self, bot):
        self.bot = bot

    def choose(self, l):
        pic = random.choice(l)
        toSend = pic['src']
        return toSend

    @commands.group(pass_context=True)
    async def nsfw(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Tag sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "nsfw channel (mention channel name)",
                            value="Create a new tag!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "nsfw everyone (True of False)",
                            value="Set if everyone can use nsfw commands or not!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "ass", value="View some ass? lol", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "tits", value="View some tits, why not?",
                            inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "nsfw view", value="View sour channel's settings.",
                            inline=False)
            await self.bot.say(embed=embed)

    @nsfw.command(pass_context=True)
    async def channel(self, ctx):
        if ctx.message.author.server_permissions.manage_server == True or ctx.message.author.id == '156517655669374977':
            if len(ctx.message.channel_mentions) == 0:
                await self.bot.say("You must mention a channel!")
            else:
                name = ctx.message.channel_mentions[0].name
                connectnsfw()
                if checkIfChangedNSFW(ctx.message.server.id):
                    conn = sqlite3.connect("nsfw.db")
                    cur = conn.cursor()
                    cur.execute("UPDATE nsfw SET guildid=?, channel=?",
                                (ctx.message.server.id, ctx.message.channel_mentions[0].name))
                    conn.commit()
                    conn.close()
                    await self.bot.say("Updated NSFW settings.")
                else:
                    conn = sqlite3.connect("nsfw.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO nsfw VALUES(?, ?)",
                                (ctx.message.server.id, ctx.message.channel_mentions[0].name))
                    conn.commit()
                    conn.close()
                    await self.bot.say("Updated NSFW settings.")
        else:
            await self.bot.say("You must have server manage permissions to use this command!")

    @nsfw.command(pass_context=True)
    async def view(self, ctx):
        await self.bot.say("Your channel to receive NSFW commands is " + getNSFWchan(ctx.message.server.id))
        if getNSFWeo(ctx.message.server.id):
            toSend = "Everyone can use NSFW commands!"
        else:
            toSend = "No one can use NSFW commands!"
        await self.bot.say(toSend)

    @nsfw.command(pass_context=True)
    async def everyone(self, ctx, bool=None):
        if ctx.message.author.server_permissions.manage_server == True or ctx.message.author.id == '156517655669374977':
            if bool is None:
                await self.bot.say("You must enter True or False!")
            else:
                connectnsfweo()
                if bool.lower() == "true" or bool.lower() == "false":
                    if checkIfChangedNSFWEO(ctx.message.server.id):
                        conn = sqlite3.connect("nsfw.db")
                        cur = conn.cursor()
                        cur.execute("UPDATE nsfweo SET guildid=?, everyone=?", (ctx.message.server.id, bool.lower()))
                        conn.commit()
                        conn.close()
                        await self.bot.say("Updated NSFW settings.")
                    else:
                        conn = sqlite3.connect("nsfw.db")
                        cur = conn.cursor()
                        cur.execute("INSERT INTO nsfweo VALUES(?, ?)", (ctx.message.server.id, bool.lower()))
                        conn.commit()
                        conn.close()
                        await self.bot.say("Updated NSFW settings.")
                else:
                    await self.bot.say("You must enter either true or false")
        else:
            await self.bot.say("You must have server manage permissions to use this command!")

    @commands.command(pass_context=True)
    async def ass(self, ctx):
        if getNSFWchan(ctx.message.server.id) == ctx.message.channel.name:
            if getNSFWeo(ctx.message.server.id) == True:
                try:
                    sent = False
                    while sent is False:
                        url = "http://thechive.com/2017/04/11/im-in-the-business-of-booty-scoops-and-business-is-a-boomin-33-photos/"
                        response = requests.get(url)
                        soup = BeautifulSoup(response.content, 'html.parser')
                        pics = list(soup.find_all('img'))
                        pic = random.choice(pics)
                        toSend = pic['src']
                        if 'thechive' in toSend:
                            sent = True
                        else:
                            sent = False
                    await self.bot.say(toSend)
                except:
                    await self.bot.say(toSend(pics))
            else:
                await self.bot.say("Not everyone can use this command in your server!")
        else:
            await self.bot.say("You can not use NSFW commands in this channel!")

    @commands.command(pass_context=True)
    async def tits(self, ctx):
        if getNSFWchan(ctx.message.server.id) == ctx.message.channel.name:
            if getNSFWeo(ctx.message.server.id) == True:
                try:
                    url = 'http://api.oboobs.ru/boobs/0/1/random'
                    response = urllib.request.urlopen(url)
                    encoding = response.info().get_content_charset('utf8')
                    data = json.loads(response.read().decode(encoding))
                    toSend = data[0]['preview']
                    toSendFile = "http://media.oboobs.ru/" + toSend
                    await self.bot.say(toSendFile)
                except Exception as e:
                    print(str(e))
            else:
                await self.bot.say("Not everyone can use this command in your server!")
        else:
            await self.bot.say("You can not use NSFW commands in this channel!")


def setup(bot):
    bot.add_cog(NSFW(bot))
