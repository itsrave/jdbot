import asyncio
import discord
from discord.ext import commands
import random
from fun.nickgen import nickgen


def randomnumber():
    number = str(random.randint(0, 100))
    return number


class Fun:
    def __init__(self, client):
        self.client = client

    # just simple funny text commands
    @commands.command()
    async def jd(self):
        await self.client.say('Jebiesz Disa na {}%!'.format(randomnumber()))

    @commands.command()
    async def zjeb(self):
        await self.client.say('Jesteś zjebem w {}%!'.format(randomnumber()))

    @commands.command(pass_context=True)
    async def nick(self, ctx):
        user = ctx.message.author
        await self.client.change_nickname(user, nickgen())

    @commands.command(pass_context=True)
    async def usunnick(self, ctx):
        user = ctx.message.author
        await self.client.change_nickname(user, None)

    # zdjecia
    @commands.command(pass_context=True)
    async def marciniak(self, ctx):
        channel = ctx.message.channel
        await self.client.send_file(channel, 'img/marcin.gif')

    @commands.command(pass_context=True)
    async def leno(self, ctx):
        try:
            channel = ctx.message.author.voice.voice_channel
            voice = await self.client.join_voice_channel(channel)
            player = voice.create_ffmpeg_player('sound/leno.wav', after=lambda: autoleave(voice))
            player.start()
            await self.client.say('LENOOO PALLENOOOOO')
            await self.client.say('SOLEZALIAAAAA')
            await self.client.say('PALENO CZAPCZANOOOOO')
        except discord.errors.ClientException:
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = vc.create_ffmpeg_player('sound/leno.wav')
            player.start()
            await self.client.say('LENOOO PALLENOOOOO')
            await self.client.say('SOLEZALIAAAAA')
            await self.client.say('PALENO CZAPCZANOOOOO')

    @commands.command(pass_context=True)
    async def szybciej(self, ctx):
        try:
            channel = ctx.message.author.voice.voice_channel
            voice = await self.client.join_voice_channel(channel)
            player = voice.create_ffmpeg_player('sound/szybciej.wav', after=lambda: autoleave(voice))
            player.start()
        except discord.errors.ClientException:
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = vc.create_ffmpeg_player('sound/szybciej.wav')
            player.start()

    @commands.command(pass_context=True)
    async def masno(self, ctx):
        try:
            channel = ctx.message.author.voice.voice_channel
            voice = await self.client.join_voice_channel(channel)
            player = voice.create_ffmpeg_player('sound/masno.mp3', after=lambda: autoleave(voice))
            player.start()
        except discord.errors.ClientException:
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = vc.create_ffmpeg_player('sound/masno.mp3')
            player.start()


def autoleave(voice):
    loop = voice.loop
    asyncio.run_coroutine_threadsafe(voice.disconnect(), loop)


def setup(client):
    client.add_cog(Fun(client))
