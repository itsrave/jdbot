#!/usr/bin/python3
# -*- coding: utf-8 -*-

import discord
import asyncio
from discord.ext import commands
from apikey.key import *

# your apikey and command prefix
TOKEN = gettoken()

client = commands.Bot(command_prefix='./')

extensions = ['fun.fun', 'sound.music', 'fun.roast', 'fun.champion']


# ready info


@client.event
async def on_ready():
    print('JDbot v0.5')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')
    await client.change_presence(game=discord.Game(name='Ruchanie matek, najczesciej twojej'))


@client.event
async def on_command_error(error, ctx):
    print(error, ctx)


@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))


@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))


@client.command()
async def reload():
    for extension in extensions:
        try:
            client.unload_extension(extension)
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))


# externsion loading
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    client.run(TOKEN)
