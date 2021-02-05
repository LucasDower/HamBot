import discord
from hambot_util import get_embed
from re import match, search
from random import randint, choice


class PassTheWord:

    emojis = {"thumbsup": '\U0001F44D', "thumbsdown": '\U0001F44E'}
    starters = ["there", "the", "once", "it"]
    players = []
    game_over = False

    message_regex = '^[a-zA-z]+\'?[a-zA-z]*[,.]?$'

    @classmethod
    async def create_from_reactions(self, ctx, join_message):
        player_ids = set()
        new_join_message = await ctx.channel.fetch_message(join_message.id)
        for reaction in new_join_message.reactions:
            async for user in reaction.users():
                player_ids.add(user.id)
        await new_join_message.clear_reactions()
        await new_join_message.edit(embed=get_embed("React to this message with any emoji to join the game.\n\nStart the game with `::pass_the_word !`.", colour=discord.Colour.from_rgb(47, 49, 54)))
        if len(player_ids) < 2:
            raise AssertionError("You need at least two players.")
        await self.create(ctx, list(player_ids))
        return self

    @classmethod
    async def create_from_mentions(self, ctx, args):
        player_ids = set()
        for arg in args:
            user_id = search('<@!([0-9]*)>', arg)
            if user_id:
                player_ids.add(int(user_id.group(1)))
        if len(player_ids) < 2:
            raise AssertionError("You need at least two players.")
        await self.create(ctx, list(player_ids))
        return self

    @classmethod
    async def create(self, ctx, player_ids):
        self.players = []
        for player_id in player_ids:
            player = discord.utils.find(lambda m: m.id == player_id, ctx.guild.members)
            self.players.append(player)

        self.num_players = len(self.players)
        self.num_candidates = self.num_players - 1
        self.chain = [choice(self.starters)]
        self.current_player_index = randint(0, self.num_players - 1)
        self.channel = ctx.channel
        for p in self.players:
            print(p.name)
        await self.message_current_player(self)
        await self.channel.send(embed=get_embed("Let the chaos ensue. When the chain is long enough, it will be posted here."))
        return self

    def update_current_player(self):
        next_player_offset = randint(1, self.num_candidates)
        self.current_player_index = (self.current_player_index + next_player_offset) % self.num_players

    async def message_current_player(self):
        current_player = self.players[self.current_player_index]
        current_prompt = ' '.join(self.chain[-2:])
        await current_player.send(embed=get_embed(f"It's your turn. What word should come next in the story after:\n```{current_prompt}```\nReply with `::chain <word>` or end the story with `::chain !`."))

    async def received_new_word(self, ctx, word):
        # Ensure the word is from someone in the game
        if self.game_over:
            return

        if not any(player.id == ctx.author.id for player in self.players):
            await ctx.send(embed=get_embed("You're not apart of the game."))
            return
        
        current_player = self.players[self.current_player_index]

        # Ensure the word is from the current player
        if ctx.author.id != current_player.id:
            await ctx.send(embed=get_embed("It's not your turn."))
            return

        # End the game if necessary
        if word == "!":
            await ctx.message.add_reaction(self.emojis['thumbsup'])
            await self.channel.send(embed=get_embed(f"Here's the final story:```{' '.join(self.chain)}```"))
            for player in self.players:
                await player.send(embed=get_embed(f"Check out the final story in **{self.channel.name}** in **{self.channel.guild.name}**"))
            self.game_over = True
            return

        # Ensure the word is legitimate
        if not match(self.message_regex, word):
            await ctx.message.add_reaction(self.emojis['thumbsdown'])
            return

        # Update current player and message them
        self.chain.append(word)
        self.update_current_player()
        await self.message_current_player()
        await ctx.message.add_reaction(self.emojis['thumbsup'])