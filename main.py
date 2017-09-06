import sqlite3

import discord
from discord.ext import commands

from utils import *


async def get_pre(bot, message):
    connect()
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (message.server.id,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return "!"
    else:
        try:
            return [(rows[0][1]), "!"]
        except:
            print("f")
            return "!"


startup_extensions = ["cog_prefix", "cog_tags", "cog_custom", "cog_info", "cog_nsfw", "cog_blacklist"]
description = '''An extension to Ardent bot, with tags, custom commands and NSFW.'''
bot = commands.Bot(command_prefix=get_pre, description=description)

bot.remove_command("help")
main_chan = discord.Object('354278428125429760')

ardent = discord.Object('354784046468956171')
@bot.event
async def on_server_join(server):
    try:
        invites = await bot.invites_from(server)
        for invite in invites:
            if not invite.revoked:
                code = invite.code
                break
    except Exception:
        code = "I couldn't grab an invite."
    await bot.send_message(ardent, '[`' + str(datetime.datetime.now().strftime(
        "%d/%m/%y %H:%M:%S")) + '`] I joined the server `' + server.name + '` (' + server.id + '), owned by `' + server.owner.name + '#' + server.owner.discriminator + '` (' + server.owner.id + '). First invite I could find: {}'.format(
        code))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        print(str(error)+ " is not found in " + ctx.message.server.name + " issued by " + ctx.message.author.name + "#" + ctx.message.author.discriminator)
    else:
        mainchannel= discord.Object('354278428125429760')
        await bot.send_message(ardent, str(error) + " in channel " + ctx.message.channel.name + " in " + ctx.message.server.name + " issued by " + ctx.message.author.name + "#" + ctx.message.author.discriminator + ".")
@bot.event
async def on_ready():
    server_count = 0
    for s in bot.servers:
        server_count = server_count + 1
    print('Logged in as')
    print(bot.user.name)
    print("Server count " + str(server_count))
    await bot.change_presence(game=discord.Game(name="!help"))
    print('------')


@bot.event
async def on_message(message):
    connectblacklist()
    conn = sqlite3.connect("blacklist.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM list WHERE guildid=? AND userid=?", (message.server.id, message.author.id))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    if not rows:
        pass
    elif rows[0][1] == message.author.id and rows[0][0] == message.server.id:
        await bot.send_message(message.channel, "You are blacklisted from using commands!")
        return
    else:
        pass
    connectcustom()
    conn = sqlite3.connect("custom.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM custom WHERE guildid=?", (message.server.id,))
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        if message.content == row[4]:
            msgToSend = str(row[3])
            if '{tagAuthor}' in msgToSend:
                toSend = msgToSend.replace('{tagAuthor}', message.author.mention)
                if '{channel}' in msgToSend:
                    toSend1 = toSend.replace('{channel}', message.channel.name)
                    send = False
                else:
                    send = True
            else:
                send = "just send"

            if send == "just send":
                await bot.send_message(message.channel, msgToSend)
            elif send:
                await bot.send_message(message.channel, toSend)
            else:
                await bot.send_message(message.channel, toSend1)

    await bot.process_commands(message)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

token = open("token.txt", "r")
toke = token.read()
bot.run(str(toke))
