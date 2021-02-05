from hambot_util import get_embed
import discord
from random import randint, choice, shuffle
import os
import json
from math import floor
from collections import deque
from random import randint
from numpy import argmax

class TopTrumps:

    challenger = 0
    alive = []
    players = []
    decks = []
    channel = None

    @classmethod
    async def create(self, ctx, join_message):

        self = TopTrumps()
        self.channel = ctx.channel

        # Get the players
        players = set()
        refreshed_join_message = await ctx.channel.fetch_message(join_message.id)
        for reaction in refreshed_join_message.reactions:
            [players.add(user) async for user in reaction.users()]
        self.players = list(players)

        if len(self.players) < 2:
            raise AssertionError("You need at least two players.")
        
        self.challenger = randint(0, len(self.players)-1)
        self.alive = [True] * len(self.players)

        # Load and distribute cards
        with open('./resources/cards.json') as file:
            cards = json.load(file)['cards']
            shuffle(cards)
        
        #cards_pp = floor(len(cards)/len(self.players))
        cards_pp = 3

        #self.decks = []
        for i in range(0, len(self.players)):
            k = i * cards_pp
            deck = deque(cards[k:k+cards_pp])
            self.decks.append(deck)
            # Send each player's top card
            top_card = deck[0]
            await self.players[i].send(file=discord.File('./cards/' + top_card['filename']))

        await self.channel.send(embed=get_embed(f"The game is ready and you each have *{cards_pp}* cards.\n\n**{self.players[self.challenger].name}** is up first. They should choose a category and play as usual. When ready, use `::continue <category>`."))
        await self.players[self.challenger].send(embed=get_embed("You're up first. Choose a category and discuss the scores.\n\nUse `::continue <category>` to move on."))
        return self


    async def continue_game(self, ctx, category):
        if category.lower() not in ['vintage', 'quality', 'cringe', 'salt', 'endurance']:
            await self.channel.send(embed=get_embed(f"Right. **{ctx.author.name}**, what the fuck is '*{category}*'? Engage your brain and make it either:\n *vintage*, *quality*, *cringe*, *salt*, or *endurance*."))
        
        # Choose the winner
        top_cards = [cards[0] for i, cards in enumerate(self.decks) if self.alive[i]]
        scores = [top_card[category.lower()] for top_card in top_cards]
        winner_index = argmax(scores)
        winning_player = self.players[winner_index]

        # Add cards to the winner's deck
        self.decks[winner_index].extend(top_cards)

        # Remove everyone's top card
        for i in range(len(self.players)):
            if not self.alive[i]:
                return
            self.decks[i].popleft()
            if len(self.decks[i]) == 0:
                await self.channel.send(embed=get_embed(f"**{self.players[i].name}** has run out of cards."))
                print(f"{self.players[i]} is out of cards.")
                self.alive[i] = False
            else:
                # Send each alive player's top card
                top_card = self.decks[i][0]
                await self.players[i].send(file=discord.File('./cards/' + top_card['filename']))

        # Check if there is a winner
        if self.alive.count(True) == 1:
            await self.channel.send(embed=get_embed(f"The game is over. **{winning_player.name}** is the winner."))
            return True

        # Get the next player
        self.challenger = winner_index

        # Message the players
        await self.channel.send(file=discord.File('./cards/' + top_cards[winner_index]['filename']))
        await self.channel.send(embed=get_embed(f"**{winning_player.name}** won with a *{category.lower()}* score of {scores[winner_index]}.\n\nYour decks have been updated."))

        return False