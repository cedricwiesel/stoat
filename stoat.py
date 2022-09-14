import discord
import time
from discord.ext import commands
from discord.utils import get
import datetime

#help command modifier
help_command = commands.DefaultHelpCommand(
    no_category = ('Commands')
)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=("."),
    help_command = help_command,
    intents = intents
    )

#Invite Command
@bot.command(
    brief="Shows you the link to invite this bot to your server"
)
async def invite(ctx):
    await ctx.send("<Test>")

#Kick Command
@bot.command(
    brief="Kicks a user (Requires Kick Permissions)"
)
async def kick(ctx, member : discord.Member, *, reason = None) :
    if  (ctx.guild.me.permissions_in(ctx.message.channel).kick_members) and (ctx.guild.me.top_role.position > member.top_role.position):
            if member.id == 270590533880119297:
                await ctx.send("https://tenor.com/view/no-i-dont-think-i-will-captain-america-old-capt-gif-17162888")
            
            elif member.id == 810913013351055411:
                await ctx.send("https://tenor.com/view/thanos-snap-inevitable-marvel-avengers-endgame-gif-14599588")

            elif not ctx.author.permissions_in(ctx.message.channel).kick_members:
                await ctx.send("You do not have kick permissions in this server")

            elif ctx.author.top_role.position < member.top_role.position:
                await ctx.send("You do not have permission to kick this person")

            else:
                await member.kick(reason = reason)
                await ctx.send("User was successfully kicked")
    else:
        await ctx.send ("I do not have kick permissions in this server")


#Ban Command
@bot.command(
    brief="Bans a user (Requires Ban Permissions)"
)
async def ban(ctx, member : discord.Member, *, reason = None) :
    if  ctx.guild.me.permissions_in(ctx.message.channel).ban_members and ctx.guild.me.top_role.position > member.top_role.position:
            if member.id == 270590533880119297:
                await ctx.send("https://tenor.com/view/no-i-dont-think-i-will-captain-america-old-capt-gif-17162888")
            
            elif member.id == 810913013351055411:
                await ctx.send("https://tenor.com/view/thanos-snap-inevitable-marvel-avengers-endgame-gif-14599588")

            elif ctx.author.permissions_in(ctx.message.channel).ban_members:
                await ctx.send("You do not have ban permissions in this server")

            elif ctx.author.top_role.position < member.top_role.position:
                await ctx.send("You do not have permission to ban this person")

            else:
                await member.ban(reason = reason)
                await ctx.send("User was successfully banned")
    else:
        await ctx.send ("I do not have ban permissions in this server")
     
#Hey Hey Command
@bot.command(
   brief="Shows a fun GIF" 
)
async def hey(ctx):
    await ctx.send("https://tenor.com/view/hayasaka-kaguya-hey-hey-hey-shinomiya-love-is-war-gif-17143662")

#Music Command
@bot.command(
    brief= "(Doesn't) play a song"
)
async def play(ctx):
    await ctx.send("Huh? Seems like that did not work. For more Information click here: <https://bit.ly/3rUbOoS>")

#Stoat Command
@bot.command(
    brief="Shows a fun GIF"
)
async def trampoline(ctx):
    await ctx.send("https://gfycat.com/dependentknobbybengaltiger")

#Say Command
@bot.command(
    brief= "Makes the Bot say something (Requires Admin Permissions)", hidden = True
)
async def say(ctx, arg):
    if (ctx.author.id == 270590533880119297) or (ctx.author.id == 435483521193082890) or (ctx.author.id == 529480190368415784) or(ctx.author.guild_permissions.administrator): #ID von Cedric oder ID von Wendi oder Id von Sina oder Admin
        await ctx.send(arg)

    else:
        await ctx.send(".say I'm Dumb")
        time.sleep(1.5) #wait one point five seconds
        await ctx.send("Huh. Doesn't seem to work. Guess I'll need Admin Perms")

#Latency Command
@bot.command(
    brief=("Shows the bots ping")
)
async def ping(ctx):
     await ctx.send(f'Pong! **{round(bot.latency * 1000)}ms**')

#Temopvoice-System
bot.customchannels = {}

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.guild.id in bot.customchannels.keys():
        bot.customchannels[member.guild.id] = {}

    if after.channel is not None:
        if after.channel.name == "Create VC":
            if member.id in bot.customchannels[member.guild.id].keys():
                customchannel = bot.get_channel(bot.customchannels[member.guild.id][member.id])
                if customchannel:
                    if customchannel.guild.id == after.channel.guild.id:
                        await member.move_to(customchannel)
                        return

                    else:
                        await customchannel.delete()

            channel = await after.channel.category.create_voice_channel(name=f'VC of {member.display_name}',position=after.channel.position)
            await channel.set_permissions(member, connect=True, mute_members=True, manage_channels=True, manage_permissions=True)
            await member.move_to(channel)
            bot.customchannels[member.guild.id][member.id] = channel.id

    if before.channel is not None and before.channel.id in bot.customchannels[member.guild.id].values() and len(before.channel.members) == 0:
        await before.channel.delete()
        del bot.customchannels[member.guild.id][list(bot.customchannels[member.guild.id].keys())[list(bot.customchannels[member.guild.id].values()).index(before.channel.id)]]

#Message-Delete-Logger
@bot.event
async def on_message_delete(message):
	guild = message.guild
	log_channel = discord.utils.get(guild.channels, name="logs")
	if log_channel is None:
		await bot.process_commands(message)
		return
	if not message.author.bot:
		embed=discord.Embed(
			color=0xff6347,
			timestamp=datetime.datetime.utcnow(),
			description="**Deleted message**:\n{}: {}\n \n**Channel** \n{}".format(message.author.mention, message.content, message.channel.mention)
		)
		embed.set_author(name=message.author, icon_url=message.author.avatar_url)
		if len(message.attachments) > 0:
			embed.set_image(url = message.attachments[0].url)
		await log_channel.send(embed=embed)
		await bot.process_commands(message)

#Message-Edit-Logger
@bot.event
async def on_message_edit(before, after):
     if before.content != after.content:
        guild = before.guild
        log_channel = discord.utils.get(guild.channels, name="logs")
        if log_channel is None:
            await bot.process_commands(before)
            return
        if not before.author.bot:
            embed=discord.Embed(
                color=0xffd700,
                timestamp=datetime.datetime.utcnow(),
                description="**Edited message**:\n{}: {}\n \n**Channel** \n{} \n **After Message**: [Click here to see new message]({})".format(after.author.mention, before.content, after.channel.mention, after.jump_url)
            )
            embed.set_author(name=before.author, icon_url=before.author.avatar_url)
            if len(after.attachments) > 0:
                embed.set_image(url = after.attachments[0].url)
            await log_channel.send(embed=embed)
            await bot.process_commands(after)

#Leave-Logger
@bot.event
async def on_member_remove(member):
    guild = member.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await bot.process_commands()
        return
    else:
        embed=discord.Embed(
            color=0xB8860B,
            timestamp=datetime.datetime.utcnow(),
            description="**Member left**:\n{}".format(member.mention)
        )
        embed.set_author(name=member, icon_url=member.avatar_url)
        await log_channel.send(embed=embed)
        await bot.process_commands()

#Auto-Role
@bot.event
async def on_member_join(member, guild):
    welcomerole =discord.utils.get(guild.roles, name = "member" or "Member")
    if member.bot != True:
        await member.add_roles(welcomerole, reason = "Joined the Server", atomic = True)
        await bot.process_commands()

#mass-role-add
@bot.command(
    brief = "Adds a role to all users", hidden = True
)
async def massrole(ctx, arg):
    if ctx.author.guild_permissions.manage_roles:
        memberrole = discord.utils.get(ctx.guild.roles, name = arg)
        for member in ctx.guild.members:
            if member.bot != True:
                await member.add_roles(memberrole)
        await ctx.send ("https://tenor.com/view/finished-elijah-wood-lord-of-the-rings-lava-fire-gif-5894611")

#add-role
@bot.command(
    brief = "Assigns a role to you", description = "Assigns a role to you if you have the member role (Requires a Role with Name \"Member\" on your server)"
)
async def addrole(ctx, arg):
    checkmark = '\U00002705'
    addedrole = discord.utils.get(ctx.guild.roles, name = arg)
    memberrole = discord.utils.get(ctx.guild.roles, name = "Member")
    if addedrole < memberrole:
        if addedrole in ctx.author.roles:
            await ctx.send("You already have that role")
        else:
            await ctx.author.add_roles(addedrole, reason = "Used the addrole-command", atomic = True)
            await ctx.message.add_reaction(checkmark)

#remove-role
@bot.command(
    brief = "Removes a role from you"
)
async def removerole(ctx, arg):
    checkmark = '\U00002705'
    removedrole = discord.utils.get(ctx.guild.roles, name = arg)
    memberrole = discord.utils.get(ctx.guild.roles, name = "Member")
    if removedrole < memberrole:
        if not removedrole in ctx.author.roles:
            await ctx.send("You do not have that role")
        else:
            await ctx.author.remove_roles(removedrole, reason = "Used the removerole-command", atomic = True)
            await ctx.message.add_reaction(checkmark)

#role-list
@bot.command(
    brief = "Shows a list of roles you can get with .addrole"
)
async def listroles(ctx):
    memberrole = discord.utils.get(ctx.guild.roles, name = "Member")
    roles = ""
    for role in ctx.guild.roles:
        if role < memberrole and role.name != "@everyone":
            roles += "-" + role.name + "\n"
    await ctx.send(roles)

#Bot Status  
@bot.event
async def on_ready():
    activity = discord.Game(name=".help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')