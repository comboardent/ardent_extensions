from utils import *
import discord
from discord.ext import commands

class Prefix():
    def __init__(self, bot):
        self.bot=bot

    @commands.group(pass_context=True)
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("You can use prefix set to set your prefix! '!' will always be there, so you can't forget it!")

    @prefix.command(pass_context=True)
    async def set(self, ctx, prefix=None):
        if ctx.message.author.server_permissions.manage_server == True:
            if prefix is not None:
                if checkIfChanged(ctx.message.server.id):
                    connect()
                    conn = sqlite3.connect("settings.db")
                    cur = conn.cursor()
                    cur.execute("UPDATE prefix SET prefix=? WHERE guildid=?", (str(prefix), ctx.message.server.id))
                    conn.commit()
                    conn.close()
                    await self.bot.say("Successfully changed your prefix to " + prefix)
                else:
                    connect()
                    conn = sqlite3.connect("settings.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO prefix VALUES(?, ?)", (ctx.message.server.id, str(prefix)))
                    conn.commit()
                    conn.close()
                    await self.bot.say("Successfully changed your prefix to " + prefix + ", remember ! will always work as a prefix also.")
            else:
                await self.bot.say("You must choose a prefix to set")
        else:
            await self.bot.say("You need the manage server permissions to change the prefix.")

    @prefix.command(pass_context=True)
    async def view(self, ctx):
        await self.bot.say("Your prefix is " + getPrefix(ctx.message.server.id))

def setup(bot):
    bot.add_cog(Prefix(bot))