import asyncio
from discord.ext import commands
import discord
import os

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
            beforeargs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            server = ctx.message.server
            vc = self.client.voice_client_in(server)
            player = await vc.create_ytdl_player(url, ytdl_options={
                'default_search': 'auto'}, before_options=beforeargs,
                                                 after=lambda: asyncio.run_coroutine_threadsafe(checkqueue(server.id)))
            players[server.id] = player
            player.start()
        except AttributeError:
            beforeargs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            server = ctx.message.server
            channel = ctx.message.author.voice.voice_channel
            await self.client.join_voice_channel(channel)
            vc = self.client.voice_client_in(server)
            player = await vc.create_ytdl_player(url, ytdl_options={
                'default_search': 'auto'}, before_options=beforeargs,
                                                 after=lambda: asyncio.run_coroutine_threadsafe(checkqueue(server.id)))
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
        for queue in queues[serverid]:
            checkqueue(serverid)
            players[serverid].stop()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].resume()

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        serverid = ctx.message.server.id
        players[serverid].stop()
        await self.client.say('Video Skippped')

    @commands.command(pass_context=True)
    async def queue(self, ctx, url):
        beforeargs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        server = ctx.message.server
        vc = self.client.voice_client_in(server)
        player = await vc.create_ytdl_player(url, ytdl_options={
            'default_search': 'auto'}, before_options=beforeargs, after=lambda: checkqueue(server.id))
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await self.client.say('Video queued')

    # playlist

    @commands.group(pass_context=True)
    async def playlist(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.client.say('Avaiable subcommands:create, delete, add ,remove')

    @playlist.command(pass_context=True)
    async def create(self, ctx, plsname):
        server = ctx.message.server
        path = os.getcwd()
        dirpath = path + "/sound/playlist/" + server.id
        try:
            os.mkdir(dirpath)
        except FileExistsError:
            pass
        if os.path.isfile("{}/{}.txt".format(dirpath, plsname)) is True:
            await self.client.say("Playlist \'{}\' already exist, choose another name.".format(plsname))
        else:
            open("{}/{}.txt".format(dirpath, plsname), 'a').close()
            await self.client.say("Playlist \'{}\' created!".format(plsname))

    @playlist.command(pass_context=True)
    async def delete(self, ctx, plsname):
        server = ctx.message.server
        path = os.getcwd()
        dirpath = path + "/sound/playlist/" + server.id
        if os.path.isfile("{}/{}.txt".format(dirpath, plsname)) is False:
            await self.client.say("Playlist \'{}\' doesn't exist.".format(plsname))
        else:
            os.remove("{}/{}.txt".format(dirpath, plsname))
            await self.client.say("Playlist \'{}\' succefully delete.".format(plsname))

    @playlist.command(pass_context=True)
    async def add(self, ctx, plsname, link):
        server = ctx.message.server
        path = os.getcwd()
        dirpath = path + "/sound/playlist/" + server.id
        if os.path.isfile("{}/{}.txt".format(dirpath, plsname)) is True:
            file = open("{}/{}.txt".format(dirpath, plsname), 'a')
            file.write(link + "\n")
            file.close()
            await self.client.say("Added {} to playlist \'{}\'".format(link, plsname))
        else:
            await self.client.say("Playlist \'{}\' doesn't exist.".format(plsname))

    @playlist.command(pass_context=True)
    async def remove(self, ctx, plsname, link):
        server = ctx.message.server
        path = os.getcwd()
        dirpath = path + "/sound/playlist/" + server.id
        if os.path.isfile("{}/{}.txt".format(dirpath, plsname)) is True:
            file = open("{}/{}.txt".format(dirpath, plsname, ), 'r')
            filedata = file.read()
            file.close()
            newdata = filedata.replace(link + "\n", "")
            file = open("{}/{}.txt".format(dirpath, plsname, ), 'w')
            file.write(newdata)
            file.close()
            await self.client.say("Removed {} from playlist \'{}\'".format(link, plsname))
        else:
            await self.client.say("Playlist \'{}\' doesn't exist.".format(plsname))

    @playlist.command(pass_context=True)
    async def view(self, ctx, plsname):
        server = ctx.message.server
        path = os.getcwd()
        dirpath = path + "/sound/playlist/" + server.id
        if os.path.isfile("{}/{}.txt".format(dirpath, plsname)) is True:
            file = open("{}/{}.txt".format(dirpath, plsname), 'r')
            filedata = file.read()
            file.close()
            await self.client.say("{}".format(filedata))
        else:
            await self.client.say("Playlist \'{}\' doesn't exist.".format(plsname))

    # @playlist.command(pass_context=True)
    # async def play(self, ctx, plsname):
    #     server = ctx.message.server
    #     path = os.getcwd()
    #     dirpath = path + "/sound/playlist/" + server.id
    #     file = open("{}/{}.txt".format(dirpath, plsname))
    #     lines = file.readlines()
    #     for link in lines:
    #         if link.startswith('https://'):
    #             beforeargs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    #             vc = self.client.voice_client_in(server)
    #             player = await vc.create_ytdl_player(link, ytdl_options={
    #                 'default_search': 'auto'}, before_options=beforeargs, after=lambda: checkqueue(server.id))
    #             if server.id in queues:
    #                 queues[server.id].append(player)
    #             else:
    #                 queues[server.id] = [player]
    #             await self.client.say('Video queued: {}'.format(link))
    #         else:
    #             pass


def setup(client):
    client.add_cog(Music(client))
