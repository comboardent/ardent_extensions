import datetime
import sqlite3
import time

def connectblacklist():
    conn = sqlite3.connect("blacklist.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS list (guildid text, userid text, name text)")
    conn.commit()
    conn.close()

def checkIfAlreadyIn(serverid, userid):
    conn = sqlite3.connect("blacklist.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM list WHERE guildid=? AND userid=?", (serverid, userid))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False

def checkIfOut(serverid, userid):
    conn = sqlite3.connect("blacklist.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM list WHERE guildid=? AND userid=?", (serverid, userid))
    rows = cur.fetchall()
    conn.close()
    if any(userid in rows for s in rows):
        return False
    else:
        return True



def connectcustom():
    conn = sqlite3.connect("custom.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS custom (guildid text, prefix text, name text, content text, combined text)")
    conn.commit()
    conn.close()

def connectnsfw():
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS nsfw (guildid text, channel text)")
    conn.commit()
    conn.close()

def connectnsfweo():
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS nsfweo (guildid text, everyone text)")
    conn.commit()
    conn.close()

def connect():
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS prefix (guildid text, prefix string)")
    conn.commit()
    conn.close()


def connecttags():
    conn = sqlite3.connect("tags.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tag (guildid text, name string, content text)")
    conn.commit()
    conn.close()


def getTime():
    currenttime = time.time()
    datetim = datetime.datetime.fromtimestamp(currenttime).strftime('%c')
    return datetim


def checkIfChanged(id):
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False

def checkIfChangedNSFW(id):
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nsfw WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False

def checkIfChangedNSFWEO(id):
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nsfweo WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False

def getNSFWchan(id):
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nsfw WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    try:
        return rows[0][1]
    except:
        return "Nill"

def getNSFWeo(id):
    conn = sqlite3.connect("nsfw.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM nsfweo WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()

    if rows[0][1].lower() == "true":
        return True
    else:
        return False


def getPrefix(id):
    connect()
    conn = sqlite3.connect("settings.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM prefix WHERE guildid=?", (id,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return "!"
    else:
        return str(rows[0][1])
