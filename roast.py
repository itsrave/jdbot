import random


def getline():
    line = random.choice(open('wrzuty.txt').readlines())
    return line


class Roast:
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        if message.author != self.client.user and message.content.startswith(('k' or 'c' or 'h' or 'p')):
            await self.client.send_message(message.channel, getline())


def setup(client):
    client.add_cog(Roast(client))
