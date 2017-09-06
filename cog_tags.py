from discord.ext import commands
import asyncio
from utils import *
import discord

class Tags():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def tag(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Tag sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id)+"tag create (name) (content)", value="Create a new tag!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "tag view (name)", value="View a tag!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "tag delete (name)", value="Delete a tag", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "tag viewall", value="View all the tags in your server!", inline=False)
            await self.bot.say(embed=embed)

    @tag.command(pass_context=True)
    async def create(self, ctx, name=None):
        if name is None:
            await self.bot.say("You must enter the name of the new tag!")
        else:
            args = ctx.message.content
            split = args.split(' ')
            lenName = len(split[2])
            toGet = int(12 + lenName)
            toPut = args[toGet:]
            connecttags()
            conn = sqlite3.connect("tags.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO tag VALUES(?, ?, ?)", (ctx.message.server.id, str(name), str(toPut)))
            conn.commit()
            conn.close()
            await self.bot.say("Successfully added new tag!")

    @tag.command(pass_context=True)
    async def view(self, ctx, name=None):
        if name is None:
            await self.bot.say("You must include the name of the tag you want to view!")
        else:
            connecttags()
            conn = sqlite3.connect("tags.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM tag WHERE guildid=? AND name=?", (ctx.message.server.id, str(name)))
            rows=cur.fetchall()
            conn.close()
            if not rows:
                await self.bot.say("That tag doesn't exist; make sure its spelling is correct.")
            else:
                await self.bot.say(rows[0][2])

    @tag.command(pass_context=True)
    async def delete(self, ctx, name = None):
        if name is None:
            await self.bot.say("You must include the name of the tag you want to delete!")
        else:
            connecttags()
            conn = sqlite3.connect("tags.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM tag WHERE guildid=? AND name=?", (ctx.message.server.id, str(name)))
            conn.commit()
            conn.close()
            await self.bot.say(f"Successfully deleted {str(name)}")

    @tag.command(pass_context=True)
    async def viewall(self, ctx):
        connecttags()
        conn = sqlite3.connect("tags.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM tag WHERE guildid=?", (ctx.message.server.id,))
        rows = cur.fetchall()
        conn.close()
        if not rows:
            await self.bot.say("Your server doesn't have any tags")
        else:
            msgToSend = ""
            x = 0
            for row in rows:
                msgToSend += (str(x) + ") " + str(row[1]) + "\n")
                x += 1
            await self.bot.say(msgToSend)



def setup(bot):
    bot.add_cog(Tags(bot))