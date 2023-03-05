import discord
from discord import app_commands
from discord.ext import commands
import datetime

stoat = commands.Bot(
    command_prefix='stoat',
    intents=discord.Intents.all()
)


misc = app_commands.Group(name="misc", description="miscellaneous commands")


# say command
@misc.command(name="say", description="makes the bot say anything")
@app_commands.describe(message="message you want the bot to send")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("sending...", ephemeral=True)
    await interaction.channel.send(message)


# ping command
@misc.command(name="ping", description="shows the bots ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send(f"Pong! **{round(stoat.latency * 1000)}ms**", ephemeral=True)


stoat.tree.add_command(misc)


# role commands
roles = app_commands.Group(name="role", description="use this to manage your roles")


# add role command
@roles.command(name="add", description="gives you one of the servers roles (has to be below the \"Custom Roles\" role)")
@app_commands.describe(role="the role you want added")
async def addrole(interaction: discord.Interaction, role: str):
    try:
        addedrole = discord.utils.get(interaction.guild.roles, name=role)
        memberrole = discord.utils.get(interaction.guild.roles, name="Custom Roles")
        if addedrole < memberrole:
            if addedrole in interaction.user.roles:
                await interaction.response.send_message("You already have that role", ephemeral=True)
            else:
                await interaction.user.add_roles(addedrole, reason="Used the addrole-command", atomic=True)
                await interaction.response.send_message("Done", ephemeral=True)
    except Exception as no:
        await interaction.response.send_message(
            "Either there is no role with that name or I do not have permission to add it to you", ephemeral=True)


# remove role command
@roles.command(name="remove", description="removes a role from you (has to be below the \"Custom Roles\" role)")
@app_commands.describe(role="the role you want removed")
async def removerole(interaction: discord.Interaction, role: str):
    removedrole = discord.utils.get(interaction.guild.roles, name=role)
    memberrole = discord.utils.get(interaction.guild.roles, name="Custom Roles")
    if removedrole < memberrole:
        if not removedrole in interaction.user.roles:
            await interaction.response.send_mnessage("You do not have that role", ephemeral=True)
        else:
            await interaction.user.remove_roles(removedrole, reason="Used the removerole-command", atomic=True)
            await interaction.response.send_message("Done", ephemeral=True)


# role list command
@roles.command(name="list",
                    description="shows a list of all the roles available for the `/role add` and `/role remove` commands")
async def rolelist(interaction=discord.Interaction):
    memberrole = discord.utils.get(interaction.guild.roles, name="Custom Roles")
    roles = ""
    for role in interaction.guild.roles:
        if role < memberrole and role.name != "@everyone":
            roles += "-" + role.name + "\n"
    await interaction.response.send_message(roles, ephemeral=True)


stoat.tree.add_command(roles)


# passive systems


# temp voice system


stoat.customchannels = {}


@stoat.event
async def on_voice_state_update(member, before, after):
    if not member.guild.id in stoat.customchannels.keys():
        stoat.customchannels[member.guild.id] = {}

    if after.channel is not None:
        if after.channel.name == "Create VC":
            if member.id in stoat.customchannels[member.guild.id].keys():
                customchannel = stoat.get_channel(stoat.customchannels[member.guild.id][member.id])
                if customchannel:
                    if customchannel.guild.id == after.channel.guild.id:
                        await member.move_to(customchannel)
                        return

                    else:
                        await customchannel.delete()

            channel = await after.channel.category.create_voice_channel(name=f'VC of {member.display_name}', position=after.channel.position)
            await channel.set_permissions(member, connect=True, mute_members=True, manage_channels=True, manage_permissions=True)
            await member.move_to(channel)
            stoat.customchannels[member.guild.id][member.id] = channel.id

    if before.channel is not None and before.channel.id in stoat.customchannels[member.guild.id].values() and len(before.channel.members) == 0:
        await before.channel.delete()
        del stoat.customchannels[member.guild.id][list(stoat.customchannels[member.guild.id].keys())[list(stoat.customchannels[member.guild.id].values()).index(before.channel.id)]]


# Message-Delete-Logger
@stoat.event
async def on_message_delete(message):
    guild = message.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await stoat.process_commands(message)
        return
    if not message.author.stoat:
        embed = discord.Embed(
            color=0xff6347,
            timestamp=datetime.datetime.utcnow(),
            description="**Deleted message**:\n{}: {}\n \n**Channel** \n{}".format(message.author.mention,
                                                                                   message.content,
                                                                                   message.channel.mention)
        )
        embed.set_author(name=message.author, icon_url=message.author.display_avatar)
        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        await log_channel.send(embed=embed)
        await stoat.process_commands(message)


# Message-Edit-Logger
@stoat.event
async def on_message_edit(before, after):
    if before.content != after.content:
        guild = before.guild
        log_channel = discord.utils.get(guild.channels, name="logs")
        if log_channel is None:
            await stoat.process_commands(before)
            return
        if not before.author.stoat:
            embed = discord.Embed(
                color=0xffd700,
                timestamp=datetime.datetime.utcnow(),
                description="**Edited message**:\n{}: {}\n \n**Channel** \n{} \n **After Message**: [Click here to see new message]({})".format(
                    after.author.mention, before.content, after.channel.mention, after.jump_url)
            )
            embed.set_author(name=before.author, icon_url=before.author.display_avatar)
            if len(after.attachments) > 0:
                embed.set_image(url=after.attachments[0].url)
            await log_channel.send(embed=embed)
            await stoat.process_commands(after)


# Leave-Logger
@stoat.event
async def on_member_remove(member):
    guild = member.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await stoat.process_commands()
        return
    else:
        embed = discord.Embed(
            color=0xB8860B,
            timestamp=datetime.datetime.utcnow(),
            description="**Member left**:\n{}".format(member.mention)
        )
        embed.set_author(name=member, icon_url=member.display_avatar)
        await log_channel.send(embed=embed)
        await stoat.process_commands()


@stoat.event
async def on_ready():
    activity = discord.Game(name="Now updated to implement slash commands", type=3)
    await stoat.change_presence(status=discord.Status.online, activity=activity)
    try:
        synced = await stoat.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


stoat.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')
