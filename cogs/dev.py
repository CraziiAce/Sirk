import discord
from discord import Embed

from discord.user import User
from discord.utils import get
from discord.ext import commands
from discord.shard import ShardInfo
from discord.ext.commands import bot

import os

import psutil

import collections

import time, datetime
from datetime import datetime

from multiprocessing.connection import Client

from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

class dev(commands.Cog):
    '''Developer Commands'''
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2F3136
        
    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, name: str):
        """Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📥 Loaded extension **cogs/{name}.py**")


    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, name: str):
        """Reloads an extension. """

        try:
            self.bot.reload_extension(f"cogs.{name}")
            await ctx.send(f"🔁 Reloaded extension **cogs/{name}.py**")

        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📤 Unloaded extension **cogs/{name}.py**")
    
    @commands.is_owner()
    @commands.command()
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.send("Successfully reloaded all extensions")

    @commands.is_owner()
    @commands.command()
    async def leaveguild(self, ctx):
        '''Leave the current server.'''
        embed=discord.Embed(title='Goodbye', color=self.color)
        await ctx.send(embed=embed)
        await ctx.guild.leave()
    
    @commands.is_owner()
    @commands.command()
    async def status(self, ctx, type, *, status=None):
        '''Change the Bot Status'''
        if type == "playing":
            await self.bot.change_presence(activity=discord.Game(name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Playing {status}`')
        elif type == "listening":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Listening to {status}`')
        elif type == "watching":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {status}`')
        elif type == "bot":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"{len(self.bot.users)} users in {len(self.bot.guilds)} servers"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Watching {len(self.bot.users)} users in {len(self.bot.guilds)} servers`')
        elif type == "competing":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"{status}"))
            await ctx.send(f'<:online:758139458767290421> Changed status to `Competing in {status}`')
        elif type == "streaming":
            await self.bot.change_presence(activity=discord.Streaming(name=f"{status}", url="https://www.twitch.tv/isirk"))
            await ctx.send(f'<:streaming:769640090275151912> Changed status to `Streaming {status}`')
        elif type == "reset":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.send("<:online:758139458767290421> Reset Status")
        else:
            await ctx.send("Type needs to be either `playing|listening|watching|streaming|competing|bot|reset`")

    @commands.is_owner()
    @commands.command()
    async def dm(self , ctx, user : discord.Member, *, content):
        '''Dm a Member'''
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text="Sirk Bot | discord.gg/7yZqHfG")
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/726779670514630667.png?v=1")
        await user.send(embed=embed)
        await ctx.send(f"<:comment:726779670514630667> Message sent to {user}")
   
    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, content:str):
        '''Make the bot say something'''
        await ctx.send(content)
        
    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        cog = self.bot.get_cog("Jishaku")
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)
            
def setup(bot):
    bot.add_cog(dev(bot))
