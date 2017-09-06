import discord
from discord.ext import commands
from utils import *

class Info():
    def __init__(self, bot):
        self.bot=bot
    @commands.command(pass_context=True)
    async def help(self, ctx):

        embed = discord.Embed(title="Commands for Relic!",
                              color=ctx.message.author.color)
        embed.add_field(name="Custom",
                        value="`custom create`, `custom delete`, `custom parameters`, `custom viewall`",
                        inline=False)
        embed.add_field(name="Prefix", value="`prefix`, `prefix view`, `prefixset`",
                        inline=False)
        embed.add_field(name="Tag", value="`tag create`, `tag delete`, `tag viewall`, `tag view`",
                        inline=False)
        embed.add_field(name="NSFW", value="`ass`, `tits`, `nsfw channel (mention channel)`, `nsfw everyone (True or false)`, `nsfw view`",
                        inline=False)
        embed.add_field(name="Blacklist",value="`blacklist add @(user)`, `blacklist remove @(user)`, `blacklist view`",
                        inline=False)
        embed.set_footer(
            text="Requested by " + ctx.message.author.display_name)
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))