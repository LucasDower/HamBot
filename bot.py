import discord, datetime

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='dead'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = client.get_channel(434854836555481090)

    if message.content.startswith('::squeak'):
        #await channel.send('Squeak!')
        f = open("date.txt", "r")
        lastSent = f.readline()
        f.close()
        date = datetime.datetime.now().strftime("%d/%m/%y")
        if (message.author.id == 211669855345049601):
                await channel.send("yes master :hamster: :sweat_drops:")
                await channel.send("daily ham (" + date + ")")
                await channel.send(file=discord.File('ham.png'))
                f = open("date.txt", "w")
                f.write(date)
                f.close()
        elif (date != lastSent):
            await channel.send("daily ham (" + date + ")")
            await channel.send(file=discord.File('ham.png'))
            f = open("date.txt", "w")
            f.write(date)
            f.close()
        else:
            await channel.send("i've already hammed today :hamster:")

    if message.content.startswith('::on'):
        await channel.send("i'm awake *squeak* :hamster:")

    if message.content.startswith('::off'):
        await channel.send("i'm having a nap :hamster:")

    if message.content.startswith('::ad_say'):
        await channel.send(message.content[8:])

    if message.content.startswith('::temp_send'):
        await channel.send(file=discord.File('temp.png'))
        

client.run('NTUyMTg2ODIzMTYyNDYyMjE5.D18Hsg.9ZtXCkavtbdZdzIq11Mq401L8SE')
