import re
import time
from datetime import datetime
from os import environ as cred


import discord

TOKEN = cred['DISCORD_TOKEN']
client = discord.Client()
author_search = True
last_sriracha_message = {}
last_sriracha_lc = {}

# print('In main.py')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Sriracha | lc help'
    ))
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global author_search, author
    global last_sriracha_message
    global last_sriracha_lc

    if message.author.id == client.user.id:
        return
    elif message.author.id == 607661949194469376:  # sriracha
        last_sriracha_message[message.channel.name] = message
        # print(last_sriracha_message[message.channel.name].content)
        if re.match('^\.lc.*', message.content):
            last_sriracha_lc[message.channel.name] = message
            print('last sriracha lc: ' + last_sriracha_lc[message.channel.name].content)
        return

    try:
        part_1 = re.match('^(.\S?)(.+)?$', message.content).groups()[0]
        part_2 = re.match('^(.\S?)(.+)?$', message.content).groups()[1]
    except AttributeError:
        return

    if part_1.lower() == 'en':
        await last_sriracha_message[message.channel.name].add_reaction('🇺🇸')
        return
    elif part_1.lower() == 'jp':
        await last_sriracha_message[message.channel.name].add_reaction('🇯🇵')
        return
    elif part_1.lower() == 'lc':
        if not part_2:
            await message.channel.send('sauce lc 3#1')
            return
        elif part_2.strip() == 'move':
            await message.channel.send("sauce move 3#1 4")
            return
        elif part_2.strip() == 'help':
            embed = discord.Embed(
                title='Commands',
                description='`lc`: equivalent to `sauce lc 3#1`.\n\n'
                '`lc move`: equivalent to `sauce move 3#1 4`.\n\n'
                '`lc asearch [on | off]`: turns automatic author search on or off (does `sauce -qa [author]` when License Checker identifies the author).\n\n'
                '`lc retry`: repeats Sriracha\'s last `.lc` command in the channel. Use if License Checker freezes on a search.\n\n'
                '`lc help` : this.\n\n'
                '`[en | jp]`: reacts with 🇺🇸 or 🇯🇵 to the last Sriracha message in the channel.\n\n',
                color=discord.Color.from_rgb(171, 110, 71),
                timestamp=datetime.now()
            )
            embed.set_author(
                name='LC streamliner',
                icon_url='https://cdn.discordapp.com/avatars/755803753000730725/3d3632c3ebc7a5ac3fffeb20387f4d40.png?size=256'
            )
            embed.set_footer(
                text='Made by Plurmp McFlurnten#7538',
                icon_url='https://cdn.discordapp.com/avatars/286339479910875136/2a9e61a6c9d706522a725ba15f3ed2d3.png?size=256'
            )
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/755803753000730725/3d3632c3ebc7a5ac3fffeb20387f4d40.png?size=256'
            )
            await message.channel.send(embed=embed)
            return
        elif part_2.strip() == 'retry':
            try:
                await message.channel.send(last_sriracha_lc[message.channel.name].content)
            except NameError:
                await message.channel.send('Retry failed')
            return
        elif (as_toggle := re.match('^asearch (.+?)$', message.content).groups()[0]) is not None:
            if as_toggle == 'on':
                author_search = True
                await message.channel.send("Author search on")
                return
            elif as_toggle == 'off':
                author_search = False
                await message.channel.send("Author search off")
                return
            else:
                await message.channel.send('On or off my guy')
                return

    if message.author.id == 661826254215053324 \
            and (author := re.match('^Looking up .+? by (.+?)\.$', message.content).groups()[0]) is not None \
            and author_search:
        # author ID is for License Checker
        await message.channel.send('Author detected')
        if author == ():
            await message.channel.send('Could not get author')
            return
        else:
            time.sleep(2)
            await message.channel.send(f'sauce -qa {author}')
            return


client.run(TOKEN)
