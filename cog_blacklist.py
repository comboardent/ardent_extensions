import discord
from utils import *
from discord.ext import commands

class Blacklist():
    def __init__(self, bot):
        self.bot=bot

    @commands.group(pass_context=True)
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Tag sub-commands", color=ctx.message.author.color)
            embed.add_field(name=getPrefix(ctx.message.server.id)+"blacklist add (name)", value="Add a user to the blacklist so they can not use any commands!!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "blacklist view", value="View all the blacklisted users in your server!", inline=False)
            embed.add_field(name=getPrefix(ctx.message.server.id) + "blacklist remove", value="Remove someone from the blacklist", inline=False)
            await self.bot.say(embed=embed)

    @blacklist.command(pass_context=True)
    async def add(self, ctx):
        if ctx.message.author.server_permissions.manage_server == True or ctx.message.author.id == '156517655669374977':
            if len(ctx.message.mentions) == 0:
                await self.bot.say("You must mention a user!")
            else:
                connectblacklist()
                if checkIfAlreadyIn(ctx.message.server.id, ctx.message.mentions[0].id):
                    await self.bot.say(f"{ctx.message.mentions[0].name} is already in the blacklist!")
                else:
                    conn = sqlite3.connect("blacklist.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO list VALUES(?, ?, ?)", (ctx.message.server.id, ctx.message.mentions[0].id, ctx.message.mentions[0].name))
                    conn.commit()
                    conn.close()
                    await self.bot.say(f"Successfully added {ctx.message.mentions[0].name} to the blacklist!")
        else:
            await self.bot.say("You don't have permissions to use this command, you need the `MANAGE SERVER` permission!")

    @blacklist.command(pass_context=True)
    async def view(self, ctx):
        connectblacklist()
        conn = sqlite3.connect("blacklist.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM list WHERE guildid=?", (ctx.message.server.id,))
        rows = cur.fetchall()
        conn.close()
        msg = ""
        if not rows:
            await self.bot.say("You don't have any blacklisted users!")
        else:
            for x in range(len(rows)):
                msg += (str(x + 1) + ") " + rows[x][2] + "\n")
            await self.bot.say(msg)

    @blacklist.command(pass_context=True)
    async def remove(self, ctx):
        if ctx.message.author.server_permissions.manage_server == True or ctx.message.author.id == '156517655669374977':
            if len(ctx.message.mentions) == 0:
                await self.bot.say("You must mention a user!")
            else:
                connectblacklist()
                if not checkIfOut(ctx.message.server.id, ctx.message.mentions[0].id):
                    await self.bot.say(f"{ctx.message.mentions[0].name} is not in the blacklist!")
                else:
                    conn = sqlite3.connect("blacklist.db")
                    cur = conn.cursor()
                    cur.execute("DELETE FROM list WHERE guildid=? AND userid=?",(ctx.message.server.id, ctx.message.mentions[0].id))
                    conn.commit()
                    conn.close()
                    await self.bot.say(f"Successfully removed {ctx.message.mentions[0].name} from the blacklist!")
        else:
            await self.bot.say("You don't have permissions to use this command, you need the `MANAGE SERVER` permission!")


def setup(bot):
    bot.add_cog(Blacklist(bot))