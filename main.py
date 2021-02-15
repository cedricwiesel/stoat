import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/rolemod'):
        await message.channel.send('https://drive.google.com/file/d/1NaXSasSYgwgTnxcuvH5Veo2rD1Mx4e5I/view?usp=sharing')
    
    if message.content.startswith('/sheriffmod'):
        await message.channel.send('https://drive.google.com/file/d/1ix81RYmDDvb0uqv1RfOWbWpUbrqUeY0c/view?usp=sharing')

    if message.content.startswith('/proximitymod'):
        await message.channel.send('https://github.com/ottomated/CrewLink/releases')

    if message.content.startswith('/p '):
        await message.channel.send('Huh? Seems like that did not work. For more Information click here: <https://bit.ly/3rUbOoS>')

client.run('ODEwOTEzMDEzMzUxMDU1NDEx.YCqjmA.uB9sySB3IA60i1dLGgQen9Keopw')