import re
from os import environ as cred

import discord

TOKEN = cred['DISCORD_TOKEN']
client = discord.Client()
author_search = True

print('In main.py')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global author_search

    if message.author.id == client.user.id:
        return

    if re.findall('^l$', message.content):
        await message.channel.send('sauce lc 3#1')

    if re.findall('^l asearch .+?$', message.content):
        as_toggle = re.match('^l asearch (.+?)$', message.content).groups()[0]
        if as_toggle == 'on':
            author_search = True
            await message.channel.send("Author search on")
        elif as_toggle == 'off':
            author_search = False
            await message.channel.send("Author search off")
        else:
            print("Author search switch error")

    if message.author == '661826254215053324' and re.findall('^Looking up .+? by .+?\.$', message.content) and author_search:
        # author ID is for License Checker
        await message.channel.send('Author detected')
        author = re.match('^Looking up .+? by (.+?)\.$', message.content).groups()[0]
        if author == ():
            await message.channel.send('Could not get author')
        await message.channel.send(f'sauce -qa {author}')


client.run(TOKEN)
