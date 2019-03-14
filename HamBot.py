import discord, datetime, re, asyncio
from subprocess import Popen
from ShittyText import shittytext

client = discord.Client()

@client.event
async def on_ready():
    print('Ready')

command_prefix = "::"
allowed_channels = ["secret", "bot-channel", "general"]

def getLastDate():
    f = open("date.txt", "r")
    lastSent = f.readline()
    f.close()
    return lastSent

@client.event
async def on_message(message):
    
    if (message.author == client.user) or not (message.channel.name in allowed_channels) or not (message.content.startswith(command_prefix)):
        return

    args = message.content.split(" ")
    command = args[0][len(command_prefix):]

    if command == 'magic8ball':
        await message.channel.send("```md\nGo fuck yourself.```")
        return

    if command == 'flipacoin':
        await message.channel.send("```md\nNo.```")
        return

    if command == 'shittytext':
        argument = ' '.join(args[1:len(args)])
        if re.compile(r'[^a-zA-Z 0-9]+').search(argument) or argument == '':
            await message.channel.send("```prolog\nInvalid Argument\n```")
        else:
            print(argument)
            await message.channel.send("```css\nProcessing...\n```")
            await message.channel.send("```\n" + shittytext(argument) + "\n```")
        return

    async def postDailyHam(date):
        await message.channel.send("daily ham (" + date + ")")
        await message.channel.send(file=discord.File('ham.png'))
        f = open("date.txt", "w")
        f.write(date)
        f.close()

    if command == 'squeak':
        date = datetime.datetime.now().strftime("%d/%m/%y")
        if (message.author.name == "SinJi"):
            await message.channel.send("yes master :hamster: :sweat_drops:")
            await postDailyHam(date)
        elif (date != getLastDate()):
            await postDailyHam(date)
        else:
            await message.channel.send("i've already hammed today :hamster:")
        return

    await message.channel.send("```prolog\nInvalid Command\n```")  


f = open("token.txt", "r")
token = f.readline()
f.close()                     
client.run(token)
