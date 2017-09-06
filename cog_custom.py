import discord
from discord.ext import commands

from utils import *


class Custom():
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def custom(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Profile sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "custom create",
                            value="Create a new custom command!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "custom delete", value="Delete a custom command!",
                            inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "custom viewall",
                            value="View all of the servers custom commands!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "custom parameters",
                            value="View the variables you can use in your custom command!!", inline=False)
            await self.bot.say(embed=embed)

    @custom.command(pass_context=True)
    async def parameters(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Custom sub-commands", color=ctx.message.author.color)
            embed.add_field(name="{tagAuthor}", value="Tag the author of the message!", inline=False)
            embed.add_field(name="{channel}", value="The name of the channel!", inline=False)
            await self.bot.say(embed=embed)

    @custom.command(pass_context=True)
    async def delete(self, ctx, name=None):
        if name is None:
            await self.bot.say("You must include the name fo the command you want to delete!")
        else:
            connectcustom()
            conn = sqlite3.connect("custom.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM custom WHERE guildid=? AND name=?", (ctx.message.server.id, str(name)))
            rows = cur.fetchall()
            conn.close()
            if not rows:
                await self.bot.say("That command name doesn't exist. Make sure you aren't including the prefix.")
            else:
                conn = sqlite3.connect("custom.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM custom WHERE name=?", (name,))
                conn.commit()
                conn.close()
                await self.bot.say("Deleted that command.")

    @custom.command(pass_context=True)
    async def viewall(self, ctx):
        connectcustom()
        conn = sqlite3.connect("custom.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM custom WHERE guildid=?", (ctx.message.server.id,))
        rows = cur.fetchall()
        conn.close()
        if not rows:
            await self.bot.say("You don't have any commands!")
        else:
            msg = ""
            for row in rows:
                msg += row[4] + "\n"
            await self.bot.say(msg)

    @custom.command(pass_context=True)
    async def create(self, ctx, name=None):
        if name is None:
            await self.bot.say("You must include the name of the command!")
        else:
            await self.bot.say("What do you want the prefix of the command to be? It can not be !")
            cont = await self.bot.wait_for_message(author=ctx.message.author)
            if cont.content == "!":
                await self.bot.say("I already told you it can't be ! smh.")
            else:
                args = ctx.message.content
                split = args.split(' ')
                lenName = len(split[2])
                toGet = int(15 + len(cont.content) + lenName)
                if len(args) + 1 == toGet:
                    await self.bot.say("Your command content can't be empty!")
                else:
                    toPut = args[toGet:]
                    connectcustom()
                    conn = sqlite3.connect("custom.db")
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM custom WHERE guildid=?", (ctx.message.server.id,))
                    rows = cur.fetchall()
                    conn.close()
                    if any((cont.content) + str(name) in s for s in rows):
                        await self.bot.say("That command name already exists in your server!")
                    else:
                        conn = sqlite3.connect("custom.db")
                        cur = conn.cursor()
                        cur.execute("INSERT INTO custom VALUES(?, ?, ?, ?, ?)", (
                        ctx.message.server.id, str(cont.content), str(name), toPut, str(cont.content + name)))
                        conn.commit()
                        conn.close()
                        await self.bot.say("Created custom command!")


def setup(bot):
    bot.add_cog(Custom(bot))
