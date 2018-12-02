import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


def getembed(champ, **kwargs):
    pos = kwargs.get('pos')
    if pos is None:
        link = "https://champion.gg/champion/{}".format(champ)
        pos = ""
    else:
        link = "https://champion.gg/champion/{}/{}".format(champ, pos)
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    w = soup.find("tr", id="statistics-win-rate-row").find_next("td").find_next("td")
    winrate = w.text.strip()
    champicon = soup.find("img", class_="champ-img")
    stsummoner = soup.find("div", class_="summoner-wrapper").find_next("img", class_="possible-build")["tooltip"]
    ndsummoner = soup.find("div", class_="summoner-wrapper").find_next("img", class_="possible-build") \
        .find_next("img", class_="possible-build")["tooltip"]
    build = soup.find("div", class_="build-wrapper")
    oneitem = build.find_next("a", target="_blank")["href"]
    twoitem = build.find_next("a", target="_blank").find_next("a", target="_blank")["href"]
    threeitem = build.find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank")["href"]
    fouritem = build.find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank").find_next("a", target="_blank").find_next("a", target="_blank")["href"]
    fiveitem = build.find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank").find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank")["href"]
    sixitem = build.find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank").find_next("a", target="_blank").find_next("a", target="_blank").find_next(
        "a", target="_blank").find_next("a", target="_blank")["href"]
    runewinrate = soup.find("div", class_="build-text").find_next(
        "div", class_="build-text").find_next("div", class_="build-text").find_next(
        "div", class_="build-text").find_next("div", class_="build-text").find_next(
        "div", class_="build-text").find_next("div", class_="build-text").find_next(
        "div", class_="build-text").find_next("div", class_="build-text").find_next("div", class_="build-text")
    runecat = soup.find("div", class_="Description__Block-bJdjrS hGZpqL").find_next("div")
    onerune = soup.find("div", class_="Description__Title-jfHpQH bJtdXG")
    tworune = soup.find("div", class_="Description__Title-jfHpQH bJtdXG").find_next(
        "div", class_="Description__Title-jfHpQH bJtdXG")
    threerune = soup.find("div", class_="Description__Title-jfHpQH bJtdXG").find_next(
        "div", class_="Description__Title-jfHpQH bJtdXG").find_next("div", class_="Description__Title-jfHpQH bJtdXG")
    fourrune = soup.find("div", class_="Description__Title-jfHpQH bJtdXG").find_next(
        "div", class_="Description__Title-jfHpQH bJtdXG").find_next(
        "div", class_="Description__Title-jfHpQH bJtdXG").find_next("div", class_="Description__Title-jfHpQH bJtdXG")
    ndrunecat = soup.find("div", class_="Description__Title-jfHpQH eOLOWg")
    ndonerune = soup.find("div", class_="Description__Title-jfHpQH eOLOWg").find_next(
        "div", class_="Description__Title-jfHpQH eOLOWg")
    ndtworune = soup.find("div", class_="Description__Title-jfHpQH eOLOWg").find_next(
        "div", class_="Description__Title-jfHpQH eOLOWg").find_next("div", class_="Description__Title-jfHpQH eOLOWg")
    embed = discord.Embed(title="{} {} build".format(champ.capitalize(), pos), url=link, description="Win Rate {}".format(
        winrate), color=0x03ff00)
    embed.set_author(name="Champion.gg", icon_url="https:{}".format(champicon['src']))
    embed.set_thumbnail(url="https:{}".format(champicon['src']))
    embed.add_field(name="Most Frequent Sumoners", inline=False, value="**{}**  **{}**".format(stsummoner, ndsummoner))
    embed.add_field(name="Most Frequent Completed Build",
                    value="**{}** > **{}** > **{}** > **{}** > **{}** > **{}**"
                    .format(oneitem[38:], twoitem[38:], threeitem[38:], fouritem[38:],
                            fiveitem[38:], sixitem[38:]), inline=False)
    embed.add_field(name="Most Frequent Runes", value="**{}**".format(runewinrate.text.strip()))
    embed.add_field(name="{}".format(runecat.text), value='**{}**\n**{}**\n**{}**\n**{}**'.format(
        onerune.text, tworune.text, threerune.text, fourrune.text), inline=False)
    embed.add_field(name="{}".format(runecat.text), value='**{}**\n**{}**\n**{}**\n**{}**'.format(
        onerune.text, tworune.text, threerune.text, fourrune.text), inline=True)
    embed.add_field(name="{}".format(ndrunecat.text), value="**{}**\n**{}**".format(
        ndonerune.text, ndtworune.text), inline=True)
    embed.set_footer(text="powered by JDbot")
    return embed


class Champion:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def champion(self, ctx, champion, position=None):
        try:
            embed = getembed(champion, pos=position)
            await self.client.say(embed=embed)
        except AttributeError:
            await self.client.say("Błędna nazwa championa lub pozycji.\nUżycie: ./champion champion pozycja\n"
                                  "Wspierane pozycje: Top, Jungle, Middle, ADC, Support")

    @commands.command(pass_context=True)
    async def opgg(self, ctx, champion, position=None):
        try:
            embed = getembed(champion, pos=position)
            await self.client.say(embed=embed)
        except AttributeError:
            await self.client.say("Błędna nazwa championa lub pozycji.\nUżycie: ./champion champion pozycja\n"
                                  "Wspierane pozycje: Top, Jungle, Middle, ADC, Support")


def setup(client):
    client.add_cog(Champion(client))
