import re
import time
from os import environ as cred

import discord

TOKEN = cred['DISCORD_TOKEN']
client = discord.Client()
author_search = True
last_sriracha_message = {}

print('In main.py')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global author_search
    global last_sriracha_message

    part_1 = re.match('^(.\S?)(.+)?$', message.content).groups()[0]
    part_2 = re.match('^(.\S?)(.+)?$', message.content).groups()[1]

    if message.author.id == client.user.id:
        return
    elif message.author.id == 607661949194469376:  # sriracha
        last_sriracha_message[message.channel.name] = message
        return

    if part_1 == 'en':
        await last_sriracha_message[message.channel.name].add_reaction('🇺🇸')
        return
    elif part_1 == 'jp':
        await last_sriracha_message[message.channel.name].add_reaction('🇯🇵')
        return
    elif part_1 == 'l':
        if part_2 is None:
            await message.channel.send('sauce lc 3#1')
            return
        elif part_2.strip() == 'move':
            await message.channel.send("sauce move 3#1 4")
            return
        elif re.findall('^asearch .+?', part_2.strip()):
            as_toggle = re.match('^asearch (.+?)$', message.content).groups()[0]
            if as_toggle == 'on':
                author_search = True
                await message.channel.send("Author search on")
                return
            elif as_toggle == 'off':
                author_search = False
                await message.channel.send("Author search off")
                return
            else:
                print("Author search switch error")
                return

    if message.author.id == 661826254215053324 \
            and re.findall('^Looking up .+? by .+?\.$', message.content) \
            and author_search:
        # author ID is for License Checker
        await message.channel.send('Author detected')
        author = re.match('^Looking up .+? by (.+?)\.$', message.content).groups()[0]
        if author == ():
            await message.channel.send('Could not get author')
            return
        else:
            time.sleep(2)
            await message.channel.send(f'sauce -qa {author}')
            return


client.run(TOKEN)
