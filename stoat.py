import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json

with open("config.json") as cjason:
    config = json.load(cjason)

stoat = commands.Bot(
    command_prefix='stoat',
    intents=discord.Intents.all()
)


# help command
@stoat.tree.command(name="help", description="shows you how to use the bot")
async def helpcommand(interaction: discord.Interaction):
    embed = discord.Embed(
        description="**Stoat v1.0**\n"
                    "\n"
                    "**Temp-Voices**\n"
                    "You can enable the temp voice feature by creating a voice channel called \"Create VC\". "
                    "It will create a new voice chat for every user who joins the above mentioned VC and delete it "
                    "as soon as nobody's left in it.\n"
                    "\n"
                    "**Logging**\n"
                    "You can enable the logging feature by creating a text channel called \"logs\".\n"
                    "The bot will then send messages to it logging edited messages, deleted messages "
                    "and people leaving the server. It will also show the pre-edited message or deleted message."
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


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
    await interaction.response.send_message(f"Pong! **{round(stoat.latency * 1000)}ms**", ephemeral=True)


stoat.tree.add_command(misc)

# role commands
roles = app_commands.Group(name="role", description="use this to manage your roles")


# add role command
@roles.command(name="add", description="gives you one of the servers roles (has to be below the \"Custom Roles\" role)")
@app_commands.describe(role="the role you want added")
async def addrole(interaction: discord.Interaction, role: str):
    try:
        added_role = discord.utils.get(interaction.guild.roles, name=role)
        member_role = discord.utils.get(interaction.guild.roles, name="Custom Roles")
        if added_role < member_role:
            if added_role in interaction.user.roles:
                await interaction.response.send_message("You already have that role", ephemeral=True)
            else:
                await interaction.user.add_roles(added_role, reason="Used the addrole-command", atomic=True)
                await interaction.response.send_message("Done", ephemeral=True)
    except Exception:
        await interaction.response.send_message(
            "Either there is no role with that name or I do not have permission to add it to you", ephemeral=True)


# remove role command
@roles.command(name="remove", description="removes a role from you (has to be below the \"Custom Roles\" role)")
@app_commands.describe(role="the role you want removed")
async def removerole(interaction: discord.Interaction, role: str):
    removed_role = discord.utils.get(interaction.guild.roles, name=role)
    member_role = discord.utils.get(interaction.guild.roles, name="Custom Roles")
    if removed_role < member_role:
        if removed_role in interaction.user.roles:
            await interaction.user.remove_roles(removed_role, reason="Used the removerole-command", atomic=True)
            await interaction.response.send_message("Done", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have that role", ephemeral=True)


# role list command
@roles.command(name="list",
               description="shows a list of all the roles available for the `/role add` and "
                           "`/role remove` commands")
async def rolelist(interaction=discord.Interaction):
    member_role = discord.utils.get(interaction.guild.roles, name="Custom Roles")
    role_list = "**Server Roles**\n"
    for role in interaction.guild.roles:
        if role < member_role and role.name != "@everyone":
            role_list += "-" + role.name + "\n"
    embed = discord.Embed(
        description=role_list
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# create role command
@roles.command(name="create", description="creates new role")
@app_commands.describe(name="the name you want for the new role", colour="the color you want your role to be "
                                                                         "(has to be in hexadecimal format)")
async def create(interaction: discord.Interaction, name: str, colour: str):
    try:
        await interaction.guild.create_role(name=name, colour=discord.Colour.from_str("0x" + colour))
        await interaction.response.send_message("role created", ephemeral=True)
    except Exception:
        await interaction.response.send_message("that's not a valid color", ephemeral=True)


stoat.tree.add_command(roles)


# temp voice system


stoat.customchannels = {}


@stoat.event
async def on_voice_state_update(member, before, after):
    if not member.guild.id in stoat.customchannels.keys():
        stoat.customchannels[member.guild.id] = {}

    if after.channel is not None:
        if after.channel.name == "Create VC":
            if member.id in stoat.customchannels[member.guild.id].keys():
                custom_channel = stoat.get_channel(stoat.customchannels[member.guild.id][member.id])
                if custom_channel:
                    if custom_channel.guild.id == after.channel.guild.id:
                        await member.move_to(custom_channel)
                        return

                    else:
                        await custom_channel.delete()

            channel = await after.channel.category.create_voice_channel(name=f'VC of {member.display_name}',
                                                                        position=after.channel.position)
            await channel.set_permissions(member, connect=True, mute_members=True,
                                          manage_channels=True, manage_permissions=True)
            await member.move_to(channel)
            stoat.customchannels[member.guild.id][member.id] = channel.id

    if before.channel is not None and before.channel.id in stoat.customchannels[member.guild.id].values() and len(
            before.channel.members) == 0:
        await before.channel.delete()
        del stoat.customchannels[member.guild.id][list(stoat.customchannels[member.guild.id].keys())[
            list(stoat.customchannels[member.guild.id].values()).index(before.channel.id)]]


# Message-Delete-Logger
@stoat.event
async def on_message_delete(message):
    guild = message.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await stoat.process_commands(message)
        return
    if not message.author.bot:
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
        if not before.author.bot:
            embed = discord.Embed(
                color=0xffd700,
                timestamp=datetime.datetime.utcnow(),
                description="**Edited message**:\n{}: {}\n \n**Channel** \n{} \n **After Message**: "
                            "[Click here to see new message]({})".format(
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
    activity = discord.Game(name="Keiner mag FSL", type=3)
    await stoat.change_presence(status=discord.Status.online, activity=activity)
    try:
        synced = await stoat.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


stoat.run(config["token"])
