import asyncio
from discord.ext import commands
import discord

players = {}
queues = {}


def checkqueue(serverid):
    if queues[serverid] != []:
        player = queues[serverid].pop(0)
        players[serverid] = player
        player.start()


class Music:
    def __init__(self, client):
        self.client = client

    # join/leave

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        server = ctx.message.server
        vc = self.client.voice_client_in(server)
        await vc.disconnect()

    # youtube player
    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        try:
            beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = await vc.create_ytdl_player(url, ytdl_options={
                'default_search': 'auto'}, before_options=beforeArgs, after=lambda: asyncio.run_coroutine_threadsafe(checkqueue(server.id)))
            players[server.id] = player
            player.start()
        except AttributeError:
            beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            server = ctx.message.server
            channel = ctx.message.author.voice.voice_channel
            await self.client.join_voice_channel(channel)
            vc = self.client.voice_client_in(server)
            player = await vc.create_ytdl_player(url, ytdl_options={
                'default_search': 'auto'}, before_options=beforeArgs, after=lambda: asyncio.run_coroutine_threadsafe(checkqueue(server.id)))
            players[server.id] = player
            player.start()
    # rmffm

    @commands.command(pass_context=True)
    async def rmffm(self, ctx):
        try:
            server = ctx.message.server
            channel = ctx.message.author.voice.voice_channel
            voice = await self.client.join_voice_channel(channel)
            player = voice.create_ffmpeg_player('http://31.192.216.8:80/rmf_fm')
            players[server.id] = player
            player.start()
        except discord.errors.ClientException:
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = vc.create_ffmpeg_player('http://31.192.216.8:80/rmf_fm')
            players[server.id] = player
            player.start()

    @commands.command(pass_context=True)
    async def rmffmstop(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].stop()

    # pause stop resume
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].pause()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].stop()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].resume()

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].stop()

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        server = ctx.message.server
        vc = self.client.voice_client_in(server)
        player = await vc.create_ytdl_player(url, ytdl_options={
                'default_search': 'auto'}, before_options=beforeArgs, after=lambda: checkqueue(server.id))
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.client.say('Video queued')


def setup(client):
    client.add_cog(Music(client))