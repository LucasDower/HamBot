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

        #if len(self.players) < 2:
        #    raise AssertionError("You need at least two players.")
        
        self.challenger = randint(0, len(self.players)-1)
        self.alive = [True] * len(self.players)

        # Load and distribute cards
        with open('./resources/cards.json') as file:
            cards = json.load(file)['cards']
            shuffle(cards)
        
        #cards_pp = floor(len(cards)/len(self.players))
        cards_pp = 3

        challenger = self.players[self.challenger]
        embed_next_turn = discord.Embed(
            colour=discord.Colour.gold()
        ).set_footer(
            text=f"It's {challenger.name}'s turn.",
            icon_url=challenger.avatar_url
        )
        embed_your_turn = get_embed("**It's your turn.** Choose a category and read out the scores. Use `::continue <category>` to exchange cards.", colour=discord.Colour.green())

        #self.decks = []
        for i in range(0, len(self.players)):
            k = i * cards_pp
            deck = deque(cards[k:k+cards_pp])
            self.decks.append(deck)
            # Send each player's top card
            embed_top_card = discord.Embed(
                description=f"You have {len(deck[i])} cards. This is your top card:",
                colour=discord.Colour.gold(),
            ).set_image(url=deck[0]["url"])
            await self.players[i].send(embed=embed_top_card)
            await self.players[i].send(embed=embed_your_turn if i == self.challenger else embed_next_turn)

        await self.channel.send(embed=get_embed(f"The game is ready. Check your DMs and reply to HamBot there."))
        return self


    async def continue_game(self, ctx, category):
        if category.lower() not in ['vintage', 'quality', 'cringe', 'salt', 'endurance']:
            await self.channel.send(embed=get_embed(f"Right. **{ctx.author.name}**, what the fuck is '*{category}*'? Engage your brain and make it either:\n *vintage*, *quality*, *cringe*, *salt*, or *endurance*."))
            return

        # Choose the winner
        top_cards = [cards[0] for i, cards in enumerate(self.decks) if self.alive[i]]
        scores = [top_card[category.lower()] for top_card in top_cards]
        winner_index = argmax(scores)
        winning_player = self.players[winner_index]

        # Add cards to the winner's deck
        self.decks[winner_index].extend(top_cards)

        # Remove everyone's top card
        just_died = []
        for i in range(len(self.players)):
            if not self.alive[i]:
                return
            self.decks[i].popleft()
            if len(self.decks[i]) == 0:
                self.alive[i] = False
                just_died.append(self.players[i].name)

        # Check if there is a winner
        if self.alive.count(True) == 1:
            embed_game_over = get_embed(f"The game is over. **{winning_player.name}** is the winner.")
            [await player.send(embed=embed_game_over) for player in self.players]
            await self.channel.send(embed=embed_game_over)
            return True

        # Get the next player
        self.challenger = winner_index

        # Message the players
        embed_end_of_round = discord.Embed(
            description=f"**{winning_player.name}** won with a *{category.lower()}* score of {scores[winner_index]}.\n\n**{', '.join(just_died)}** has run out of cards and is out.",
            colour=discord.Colour.gold()).set_image(url=top_cards[winner_index]["url"])
        await self.message_players(embed_end_of_round)

        return False


    async def message_players(self, embed_end_of_round):
        challenger = self.players[self.challenger]
        embed_next_turn = discord.Embed(
            colour=discord.Colour.gold()
        ).set_footer(
            text=f"It's {challenger.name}'s turn.",
            icon_url=challenger.avatar_url
        )
        embed_your_turn = get_embed("**It's your turn.** Choose a category and read out the scores. Use `::continue <category>` to exchange cards.", colour=discord.Colour.green())

        for i in range(len(self.players)):
            player = self.players[i]
            # Message all players, alive or dead, who won the round.
            await player.send(embed=embed_end_of_round)

            # Send alive players their new card
            if not self.alive[i]:
                return
            embed_top_card = discord.Embed(
                description=f":hamster:  You have {len(self.decks[i])} cards. This is your top card:",
                colour=discord.Colour.gold(),
            ).set_image(url=self.decks[i][0]["url"])
            await player.send(embed=embed_top_card)

            await player.send(embed=embed_your_turn if i == self.challenger else embed_next_turn)
