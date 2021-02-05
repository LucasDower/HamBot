import discord
import asyncio
import datetime
import random
import os
import re
import pickle
import atexit
import requests
from HamBotUtil import get_embed, get_sentiment_score
from discord.ext import commands
from PassTheWord import PassTheWord

flags = {"good bot": ":slight_smile:",
         "bad bot": ":slight_frown:"}

games = ["Mafia City", "Destiny 2", "Blackwake", "Grand Theft Auto V", "NEKOPARA Vol. 1", "Minecraft",
         "Sea of Thieves", "Disco Elysium", "Overwatch", "Chess", "NEKOPARA Vol. 2", "NEKOPARA Vol. 0", "NEKOPARA Vol. 3", "Yandere Simulator"]
aliases = ["hambot", "ham bot", "hammy", "hamster", "hammie"]
interrogatives = ["are", "do", "can't", "did", "aren't", "you're", "don't", "cant", "arent", "youre", "will", "wont", "won't", "isnt", "isn't"]

pass_the_word_game = None
friends = set()
gif_url = "https://media1.tenor.com/images/c18a2c7a37ee1f2c618a63bb1186909f/tenor.gif"
ham_url = "https://i.imgur.com/QteKFyY.png"

bot = commands.Bot(command_prefix='::',
                   description="a shitty bot you should not take seriously",
                   activity=discord.Activity(type=discord.ActivityType.listening, name="Canon in D"))


def exit_handler():
    print("Updating friends.txt")
    with open("friends.txt", "wb") as wf:
        pickle.dump(friends, wf)


@bot.listen()
async def on_ready():
    print("Connected")

@bot.listen()
async def on_member_update(before, after):
    if not (before.status == discord.Status.offline and after.status == discord.Status.online):
        return

    if after.id in friends:
        return
    friends.add(after.id)

    embed = discord.Embed(title=":love_letter: HamBot Friendship Card",
                          type="rich",
                          description="",
                          colour=discord.Colour.red()).set_thumbnail(url=gif_url)
    embed.add_field(name="To:", value=f"{after.name}")
    embed.add_field(name="From:", value="Hammy :hearts:")
    embed.set_footer(text="This card officially declares that I love you. x", icon_url=after.avatar_url)

    await after.send(embed=embed)

    print(f"Now friends with [{after.name}]")


@bot.listen()
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.channel.type == discord.ChannelType.private:
        print(f"[{msg.author.name}] -> [HamBot]: {msg.content}")

    for flag in flags.keys():
        if flag in msg.content:
            await msg.channel.send(flags[flag])
            return

    # If the message is not addressed to HamBot, ignore it
    if not any(alias in msg.content for alias in aliases):
        return

    if msg.content.endswith('?'):
        if any(word in msg.content for word in interrogatives):
            await msg.channel.send(":hamster: %s" % (random.choice(["yes", "no"])))
            return

    score = get_sentiment_score(msg.content)
    if score > 0.35:
        await msg.channel.send(":hamster: happy squeak")
    elif score < -0.35:
        await msg.channel.send(":hamster: sad squeak")
    else:
        await msg.channel.send(":hamster: squeak")
    return


@bot.command()
async def squeak(ctx):
    today = datetime.datetime.now().strftime("%d/%m/%y")
    embed = discord.Embed(title=":hamster: squeak",
                          type="rich",
                          description=f"daily ham ({today})",
                          colour=discord.Colour.gold()
                          ).set_image(url=ham_url)
    await ctx.send(embed=embed)


@bot.command()
async def random_kick(ctx):
    members_in_voice = []
    for voice_channel in ctx.guild.voice_channels:
        members_in_voice.extend(voice_channel.members)
    if len(members_in_voice) > 0:
        unlucky_member = random.choice(members_in_voice)
        await ctx.send(embed=get_embed(f"Unlucky **{unlucky_member.name}**."))
        await unlucky_member.edit(voice_channel=None)

join_message = None

@bot.command()
async def pass_the_word(ctx, *args):
    global pass_the_word_game, join_message
    if len(args) == 0:
        join_message = await ctx.send(embed=get_embed("React to this message with any emoji to join the game.\n\nStart the game with `::pass_the_word !`.", discord.Colour.green()))
        return
    if len(args) == 1 and args[0] == "!" and join_message != None:
        try:
            pass_the_word_game = PassTheWord()
            await pass_the_word_game.create_from_reactions(ctx, join_message)
        except AssertionError as e:
            await ctx.send(embed=get_embed(str(e), discord.Colour.red()))
        except Exception as e:
            print(e)
            await ctx.send(embed=get_embed("Let Lucas know he's fucked up.", discord.Colour.red()))
    else:
        try:
            pass_the_word_game = PassTheWord()
            await pass_the_word_game.create_from_mentions(ctx, args)
        except AssertionError as e:
            await ctx.send(embed=get_embed(str(e), discord.Colour.red()))
        except Exception as e:
            print(e)
            await ctx.send(embed=get_embed("Let Lucas know he's fucked up.", discord.Colour.red()))


@bot.command()
async def chain(ctx, word):
    await pass_the_word_game.received_new_word(ctx, word)


@bot.command()
async def test(ctx):
    embed = discord.Embed(title=":love_letter: HamBot Friendship Card",
                          colour=discord.Colour.red())
    embed.set_thumbnail(url=gif_url)
    embed.add_field(name="To:", value=f"{ctx.author.name}")
    embed.add_field(name="From:", value="Hammy :hearts:")
    embed.set_footer(
        text="This card officially declares that I love you. x", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def emojify(ctx, emoji_name):
    last_message = await ctx.channel.history(limit=2).flatten()
    last_message = last_message[1]
    image_url = last_message.attachments[0].url
    r = requests.get(image_url)
    if r.status_code == 200:
        #image_bytes = r.text.encode(encoding='UTF-16')
        #print(image_bytes)
        await ctx.guild.create_custom_emoji(name=emoji_name, image=r.content)


if __name__ == '__main__':
    with open("friends.txt", "rb") as rf:
        friends = pickle.load(rf)
        print(f"I have [{len(friends)}] friends")

    atexit.register(exit_handler)

    assert "HAMBOT_TOKEN" in os.environ
    bot.run(os.environ["HAMBOT_TOKEN"])
