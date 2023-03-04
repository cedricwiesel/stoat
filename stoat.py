import discord
from discord import app_commands
from discord.ext import commands
import datetime

bot = commands.Bot(
    intents=discord.Intents.all()
)


@bot.tree.command(name="test")
async def test(interaction):
    await interaction.response.send_message(f"{interaction.user.mention} selber test")


# invite command
@bot.tree.command(name="invite", description="gives you a link to invite this bot to your server")
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://discord.com/api/oauth2/authorize?client_id=810913013351055411&permissions=8&scope=bot", ephemeral=True)


# say command
@bot.tree.command(name="say", description="makes the bot say anything")
@app_commands.describe(message="message you want the bot to send")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


# ping command
@bot.tree.command(name="ping", description="shows the bots ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! **{round(bot.latency * 1000)}ms**", ephemeral=True)


# add role command
@bot.tree.command(name="addrole",
                  description="gives you one of the servers roles (has to be below the \"Custom Roles\" role)")
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
@bot.tree.command(name="removerole", description="removes a role from you (has to be below the \"Custom Roles\" role)")
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
@bot.tree.command(name="listroles",
                  description="shows a list of all the roles available for the `/addrole` and `removerole` commands")
async def listroles(interaction=discord.Interaction):
    memberrole = discord.utils.get(interaction.guild.roles, name="Custom Roles")
    roles = ""
    for role in interaction.guild.roles:
        if role < memberrole and role.name != "@everyone":
            roles += "-" + role.name + "\n"
    await interaction.response.send_message(roles, ephemeral=True)


# passive systems


# temp voice system


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

            channel = await after.channel.category.create_voice_channel(name=f'VC of {member.display_name}',
                                                                        position=after.channel.position)
            await channel.set_permissions(member, connect=True, mute_members=True, manage_channels=True,
                                          manage_permissions=True)
            await member.move_to(channel)
            bot.customchannels[member.guild.id][member.id] = channel.id

    if before.channel is not None and before.channel.id in bot.customchannels[member.guild.id].values() and len(
            before.channel.members) == 0:
        await before.channel.delete()
        del bot.customchannels[member.guild.id][list(bot.customchannels[member.guild.id].keys())[
            list(bot.customchannels[member.guild.id].values()).index(before.channel.id)]]


# Message-Delete-Logger
@bot.event
async def on_message_delete(message):
    guild = message.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await bot.process_commands(message)
        return
    if not message.author.bot:
        embed = discord.Embed(
            color=0xff6347,
            timestamp=datetime.datetime.utcnow(),
            description="**Deleted message**:\n{}: {}\n \n**Channel** \n{}".format(message.author.mention,
                                                                                   message.content,
                                                                                   message.channel.mention)
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
        await log_channel.send(embed=embed)
        await bot.process_commands(message)


# Message-Edit-Logger
@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        guild = before.guild
        log_channel = discord.utils.get(guild.channels, name="logs")
        if log_channel is None:
            await bot.process_commands(before)
            return
        if not before.author.bot:
            embed = discord.Embed(
                color=0xffd700,
                timestamp=datetime.datetime.utcnow(),
                description="**Edited message**:\n{}: {}\n \n**Channel** \n{} \n **After Message**: [Click here to see new message]({})".format(
                    after.author.mention, before.content, after.channel.mention, after.jump_url)
            )
            embed.set_author(name=before.author, icon_url=before.author.avatar_url)
            if len(after.attachments) > 0:
                embed.set_image(url=after.attachments[0].url)
            await log_channel.send(embed=embed)
            await bot.process_commands(after)


# Leave-Logger
@bot.event
async def on_member_remove(member):
    guild = member.guild
    log_channel = discord.utils.get(guild.channels, name="logs")
    if log_channel is None:
        await bot.process_commands()
        return
    else:
        embed = discord.Embed(
            color=0xB8860B,
            timestamp=datetime.datetime.utcnow(),
            description="**Member left**:\n{}".format(member.mention)
        )
        embed.set_author(name=member, icon_url=member.avatar_url)
        await log_channel.send(embed=embed)
        await bot.process_commands()


@bot.event
async def on_ready():
    activity = discord.Game(name="Testing Slash Commands", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


bot.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')
