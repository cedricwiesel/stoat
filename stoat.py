import discord
import time
import os
from discord.ext import commands

#help command modifier
help_command = commands.DefaultHelpCommand(
    no_category = ('Commands')
)

bot = commands.Bot(
    command_prefix=("/"),
    help_command = help_command
    )

#Role Mod Command
@bot.command(
    brief="Shows the link for Among Us Role Mod"
)
async def rolemod(ctx):
    await ctx.send("<https://drive.google.com/file/d/1NaXSasSYgwgTnxcuvH5Veo2rD1Mx4e5I/view?usp=sharing>")

#Sheriff Mod Command
@bot.command(
    brief="Shows the link for Among Us Sheriff Mod"
)
async def sheriffmod(ctx):
    await ctx.send("<https://drive.google.com/file/d/1ix81RYmDDvb0uqv1RfOWbWpUbrqUeY0c/view?usp=sharing>")

#Proximity Mod Command
@bot.command(
    brief="Shows the link for Among Us Proximity Chat Mod"
)
async def proximitymod(ctx):
    await ctx.send("<https://github.com/ottomated/CrewLink/releases>")

#Invite Command
@bot.command(
    brief="Shows you the link to invite this bot to your server"
)
async def invite(ctx):
    await ctx.send("<https://discord.com/api/oauth2/authorize?client_id=810913013351055411&permissions=379910&scope=bot>")

#Kick Command
@bot.command(
    brief="Kicks a user (Requires Kick Permissions)"
)
async def kick(ctx, member : discord.Member, *, reason = None):
    if (ctx.author.permissions_in(ctx.message.channel).kick_members):
        if (member.id == 270590533880119297):
            await ctx.send("https://tenor.com/view/no-i-dont-think-i-will-captain-america-old-capt-gif-17162888")

        elif(member.id == 810913013351055411):
            await ctx.send("https://tenor.com/view/thanos-snap-inevitable-marvel-avengers-endgame-gif-14599588")

        elif (ctx.author.top_role.position < member.top_role.position):
            return await ctx.send("You do not have permission to kick this person")

        elif ctx.guild.me.top_role.position < member.top_role.position:
            return await ctx.send("I do not have permission to kick this Person")

        else:
            await member.ban(reason = reason)
            await ctx.send("User was successfully kicked")

    else:
        await ctx.send("You do not have permission to perform this action")

#Ban Command
@bot.command(
    brief="Bans a user (Requires Ban Permissions)"
)
async def ban(ctx, member : discord.Member, *, reason = None):
    if (ctx.author.permissions_in(ctx.message.channel).ban_members):
        if (member.id == 270590533880119297):
            await ctx.send("https://tenor.com/view/no-i-dont-think-i-will-captain-america-old-capt-gif-17162888")

        elif(member.id == 810913013351055411):
            await ctx.send("https://tenor.com/view/thanos-snap-inevitable-marvel-avengers-endgame-gif-14599588")

        elif (ctx.author.top_role.position < member.top_role.position):
            return await ctx.send("You do not have permission to ban this person")

        elif ctx.guild.me.top_role.position < member.top_role.position:
            return await ctx.send("I do not have permission to ban this Person")

        else:
            await member.ban(reason = reason)
            await ctx.send("User was successfully banned")

    else:
        await ctx.send("You do not have permission to perform this action")

#Hey Hey Command
@bot.command(
   brief="Shows a fun GIF" 
)
async def hey(ctx):
    await ctx.send("https://tenor.com/view/hayasaka-kaguya-hey-hey-hey-shinomiya-love-is-war-gif-17143662")

#WHO PINGED ME Command
@bot.command(
    brief="Shows a fun GIF"
)
async def stfu(ctx):
    await ctx.send("https://tenor.com/view/full-metal-jacket-who-pinged-me-gunnery-sergeant-hartman-chat-ping-pong-gif-11748348")

#Music Command
@bot.command(
    brief="(Doesn't) play a song"
)
async def p(ctx):
    await ctx.send("Huh? Seems like that did not work. For more Information click here: <https://bit.ly/3rUbOoS>")

#Stoat Command
@bot.command(
    brief="Shows a fun GIF"
)
async def trampoline(ctx):
    await ctx.send("https://gfycat.com/dependentknobbybengaltiger")

#Say Command
@bot.command(
    brief=("Makes the Bot say something (Requires Admin Permissions)")
)
async def say(ctx, arg):
    if (ctx.author.id == 435483521193082890) or (ctx.author.guild_permissions.administrator): #ID von Cedric oder ID von Wendi oder Admin
        await ctx.send(arg)

    else:
        await ctx.send("/say I'm Dumb")
        time.sleep(1.5) #wait three seconds
        await ctx.send("Huh. Doesn't seem to work. Guess I'll need Admin Perms")

#Latency Command
@bot.command(
    brief=("Shows the bots ping")
)
async def ping(ctx):
     await ctx.send(f'Pong! **{round(bot.latency * 1000)}ms**')

#Bot Status  
@bot.event
async def on_ready():
    activity = discord.Game(name="New Update! Type /help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')