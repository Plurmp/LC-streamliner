import re
import time
from datetime import datetime
from os import environ as cred

import discord

TOKEN = cred['DISCORD_TOKEN']
client = discord.Client()
author_search = True
last_sriracha_embed = {}
last_sriracha_lc = {}


# print('In main.py')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Sriracha | lc help'
    ))
    print('Logged in as {0.user}'.format(client))


def clean_args(cmd: str, args):
    try:
        return args.group(cmd)
    except AttributeError:
        return None


@client.event
async def on_message(message):
    global author_search
    global last_sriracha_embed
    global last_sriracha_lc

    print('Received message: ' + message.content)
    print('Message author: ' + message.author.name + ", " + str(message.author.id))
    print()

    if message.author.id == client.user.id:
        return
    elif message.author.id == 607661949194469376 or message.author.id == 640402425395675178:  # sriracha or oh sheet
        if message.embeds:
            last_sriracha_embed[message.channel.name] = message
        # print(last_sriracha_embed[message.channel.name].content)
        elif re.match('^\.lc.*', message.content):
            last_sriracha_lc[message.channel.name] = message
            print('last sriracha lc: ' + last_sriracha_lc[message.channel.name].content)
        return

    if message.author.id == 640402425395675178 \
            and re.findall('^Looking up .+ by .+?\.$', message.content) \
            and author_search:
        # author ID is for License Checker or oh sheet
        await message.channel.send('Author detected')
        author = re.match('^Looking up .+ by (.+?)\.$', message.content).groups()[0]
        if author == ():
            await message.channel.send('Could not get author')
            return
        else:
            time.sleep(2)
            author_fixed = re.sub('-', '~', author)
            await message.channel.send(f'sauce -qa {author_fixed}')
            return

    args = re.match(
        '^(?P<prefix>lc|qc|st|en|jp)\s*(?P<cmd>asearch|retry|move|help)?(?:\s(?P<switch>on|off))?(?:\s(?P<list_id>\d+))?$',
        message.content.strip().lower()
    )
    prefix = clean_args('prefix', args)
    cmd = clean_args('cmd', args)
    switch = clean_args('switch', args)
    list_id = clean_args('list_id', args)
    print(
        f'prefix: {prefix}\n'
        f'cmd: {cmd}\n'
        f'switch: {switch}\n'
        f'list_id: {list_id}\n'
    )

    if not prefix:
        return
    elif prefix == 'qc':
        if not cmd:
            if not list_id:
                await message.channel.send('sauce 1#1')
                return
            else:
                await message.channel.send(f'sauce 1#{list_id}')
                return
        elif cmd == 'move':
            if not list_id:
                await message.channel.send('sauce move 1#1 2')
                return
            else:
                await message.channel.send(f'sauce move 1#{list_id} 2')
                return
    elif prefix == 'st':
        if not cmd:
            if not list_id:
                await message.channel.send('sauce 2#1')
                return
            else:
                await message.channel.send(f'sauce 2#{list_id}')
                return
        elif cmd == 'move':
            if not list_id:
                await message.channel.send('sauce move 2#1 3')
                return
            else:
                await message.channel.send(f'sauce move 2#{list_id} 3')
                return
    elif prefix == 'lc':
        if not cmd:
            if not list_id:
                await message.channel.send('sauce lc 3#1')
                return
            else:
                await message.channel.send(f'sauce lc 3#{list_id}')
                return
        elif cmd == 'move':
            if not list_id:
                await message.channel.send('sauce move 3#1 4')
                return
            else:
                await message.channel.send(f'sauce move 3#{list_id} 4')
                return
        elif cmd == 'asearch':
            if switch == 'on':
                author_search = True
                await message.channel.send('Author search on')
                return
            elif switch == 'off':
                author_search = False
                await message.channel.send('Author search off')
                return
        elif cmd == 'retry':
            try:
                before_author_search = author_search
                author_search = False
                await message.channel.send(last_sriracha_lc[message.channel.name].content)
                time.sleep(2)
                author_search = before_author_search
            except NameError:
                await message.channel.send('Retry failed')
            return
        elif cmd == 'help':
            embed = discord.Embed(
                title='Commands',
                color=discord.Color.from_rgb(171, 110, 71),
                timestamp=datetime.now()
            )
            embed.add_field(
                name='QC shortcuts',
                value='`qc [id]`: equivalent to `sauce 1#[id]` (defaults to 1#1).\n\n'
                      '`qc move [id]`: equivalent to `sauce move 1#[id] 2` (defaults to 1#1).\n\n',
                inline=True
            )
            embed.add_field(
                name='Sorting shortcuts',
                value='`st [id]`: equivalent to `sauce 2#[id]` (defaults to 2#1).\n\n'
                      '`st move [id]`: equivalent to `sauce move 2#[id] 3` (defaults to 2#1).\n\n',
                inline=True
            )
            embed.add_field(
                name='LC shortcuts',
                value='`lc`: equivalent to `sauce lc 3#[id]` (defaults to 3#1).\n\n'
                      '`lc move`: equivalent to `sauce move 3#[id] 4` (defaults to 3#1).\n\n'
                      '`lc asearch [on | off]`: turns automatic author search on or off (does `sauce -qa [author]` when License Checker identifies the author).\n\n'
                      '`lc retry`: repeats Sriracha\'s last `.lc` command in the channel. Use if License Checker freezes on a search.\n\n'
                      '`lc help` : this.\n\n'
                      '`[en | jp]`: reacts with 🇺🇸 or 🇯🇵 to the last Sriracha message in the channel.\n\n',
                inline=True
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
    elif prefix == 'en':
        await last_sriracha_embed[message.channel.name].add_reaction('🇺🇸')
        return
    elif prefix == 'jp':
        await last_sriracha_embed[message.channel.name].add_reaction('🇯🇵')
        return


client.run(TOKEN)
