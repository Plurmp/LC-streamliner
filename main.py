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

    if message.author.id == client.user.id:
        return
    elif message.author.id == 607661949194469376:  # sriracha
        last_sriracha_message[message.channel.name] = message
        return

    if re.findall('^en$', message.content):
        await last_sriracha_message[message.channel.name].add_reaction('🇺🇸')
        return
    elif re.findall('^jp$', message.content):
        await last_sriracha_message[message.channel.name].add_reaction('🇯🇵')
        return

    if re.findall('^l$', message.content):
        await message.channel.send('sauce lc 3#1')
        return

    if re.findall('^l asearch .+?$', message.content):
        as_toggle = re.match('^l asearch (.+?)$', message.content).groups()[0]
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

    if re.findall('^l move$', message.content):
        await message.channel.send("sauce move 3#1 4")

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
