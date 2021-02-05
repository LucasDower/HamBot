import discord
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def get_sentiment_score(message):
    return analyser.polarity_scores(message)['compound']

def get_embed(text, colour=discord.Colour.gold()):
    return discord.Embed(description=f":hamster:  {text}", colour=colour)