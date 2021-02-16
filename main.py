import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="/")

#Role Mod Command
@bot.command(
    brief="Shows the link for Among Us Role Mod"
)
async def rolemod(ctx):
    await ctx.channel.send("<https://drive.google.com/file/d/1NaXSasSYgwgTnxcuvH5Veo2rD1Mx4e5I/view?usp=sharing>")

#Sheriff Mod Command
@bot.command(
    brief="Shows the link for Among Us Sheriff Mod"
)
async def sheriffmod(ctx):
    await ctx.channel.send("<https://drive.google.com/file/d/1ix81RYmDDvb0uqv1RfOWbWpUbrqUeY0c/view?usp=sharing>")

#Proximity Mod Command
@bot.command(
    brief="Shows the link for Among Us Proximity Chat Mod"
)
async def proximitymod(ctx):
    await ctx.channel.send("https://github.com/ottomated/CrewLink/releases")

#Invite Command
@bot.command(
    brief="Shows you the link to invite this bot to your server"
)
async def invite(ctx):
    await ctx.channel.send("https://discord.com/api/oauth2/authorize?client_id=810913013351055411&permissions=379910&scope=bot")

#Kick Command
@bot.command(
    brief="Kicks a member"
)
async def kick(ctx, member : discord.Member, *, reason = None):
    if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
        await member.kick(reason = reason)
        await ctx.channel.send("User was successfully kicked")

    else:
        await ctx.channel.send("You do not have permission to perform this action")

#Ban Command
@bot.command(
    brief="Bans a member"
)
async def ban(ctx, member : discord.Member, *, reason = None):
    if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
        await member.ban(reason = reason)
        await ctx.channel.send("User was successfully banned")

    else:
        await ctx.channel.send("You do not have permission to perform this action")

#Hey Hey Command
@bot.command(
   brief="HEY HEY!" 
)
async def hey(ctx):
    await ctx.channel.send("https://tenor.com/view/hayasaka-kaguya-hey-hey-hey-shinomiya-love-is-war-gif-17143662")

#WHO PINGED ME Command
@bot.command(
    brief="Pinging everyone is annoying"
)
async def ping(ctx):
    await ctx.channel.send("https://tenor.com/view/full-metal-jacket-who-pinged-me-gunnery-sergeant-hartman-chat-ping-pong-gif-11748348")

#Music Command
@bot.command(
    brief="Plays a song"
)
async def p(ctx):
    await ctx.channel.send("Huh? Seems like that did not work. For more Information click here: <https://bit.ly/3rUbOoS>")
    
@bot.event
async def on_ready():
    activity = discord.Game(name="/help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')