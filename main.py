import re
import time
import logging
from datetime import datetime, timezone
from os import environ as cred

import hikari
from hikari import NotFoundError
from hikari.presences import Activity, ActivityType

from dotenv import load_dotenv
load_dotenv()

TOKEN = cred['DISCORD_TOKEN']
last_sriracha_embed = {}
last_sriracha_lc = {}
bots = {
    "sriracha": 607661949194469376,
    "ohsheet": 640402425395675178,
    "lc": 661826254215053324
}

logger = logging.getLogger("Mortal Log")
ANTIBUG = logging.INFO - 5
logging.addLevelName(ANTIBUG, "INDIAN_CUSTOMER_SERVICE")

bot = hikari.GatewayBot(token=TOKEN, logs="INDIAN_CUSTOMER_SERVICE")
prefixes = ("lc", "qc", "st", "en", "jp")


def mortallog(log_message: str):
    logger.log(ANTIBUG, log_message)


def clean_args(cmd: str, args):
    try:
        return args.group(cmd)
    except AttributeError:
        return None


def is_sriracha_bot(message_event: hikari.GuildMessageCreateEvent) -> bool:
    if (
        message_event.author_id == bots["sriracha"]
        or message_event.author_id == bots["ohsheet"]
    ):
        return True
    else:
        return False


@bot.listen()
async def listen_to_us(message_event: hikari.GuildMessageCreateEvent) -> None:
    message = message_event.message

    if (
            # not message_event.content and not message_event.embeds or
            message_event.author_id == bot.get_me().id
    ):
        return

    global last_sriracha_embed
    global last_sriracha_lc

    if is_sriracha_bot(message_event):
        mortallog("Sriracha/oh sheet Bot found!")
        if message_event.embeds:
            mortallog("Has embeds!")
            last_sriracha_embed[message_event.get_channel().name] = message

            for f in message_event.embeds[0].fields:
                if (
                    f.name.strip() == "Tier"
                    and f.value.strip() == "Not set"
                    and re.match(r"ID: 3#\d", message_event.embeds[0].footer.text)
                ):
                    await message.respond("**WARNING: TIER NOT SET**")
                    return
        elif re.match(r"^\.lc.*", message.content):
            last_sriracha_lc[message_event.get_channel().name] = message
            mortallog(
                "last sriracha lc: "
                + last_sriracha_lc[message_event.get_channel().name].content
            )
        return

    if not message.content or not message.content.startswith(prefixes):
        return

    mortallog("Received message: " + str(message_event.content))
    mortallog(
        "Message author: "
        + message_event.author.username
        + ", "
        + str(message_event.author_id)
    )

    if (
        re.findall(r"^Looking up .+ by .+?\.$", message_event.content)
        and message_event.author_id == bots["ohsheet"]
    ):
        mortallog("found a match")
    else:
        mortallog("no match")
    print()

    if re.findall(r"^Looking up .+ by .+?\.$", message.content) and (
        message.author.id == bots["ohsheet"]
        or message.author.id == bots["lc"]
    ):
        mortallog("Detecting author")
        await message.respond("Author detected")
        author = re.match(r"^Looking up .+ by (?P<author>.+?)\.$",
                          message.content).group('author')

        if author == ():
            await message.respond("Could not get author")
            return
        else:
            time.sleep(3)
            author_fixed = re.sub(r"-", "~", author)
            await message.respond(f"sauce -qa {author_fixed}")
            return
    else:
        mortallog("Not searching for author...")

    args = re.match(
        r"^(?P<prefix>lc|qc|st|en|jp)\s*(?P<cmd>retry|move|help|del|delete|delet)?(?:\s(?P<list_id>\d+))?$",
        message.content.strip().lower(),
    )
    prefix = clean_args("prefix", args)
    cmd = clean_args("cmd", args)
    list_id = clean_args("list_id", args)
    mortallog(f"prefix: {prefix} | cmd: {cmd} | list_id: {list_id}")

    if not prefix:
        return

    elif prefix.lower() == "qc":
        if not cmd:
            if not list_id:
                await message.respond("sauce 1#1")
                return
            else:
                await message.respond(f"sauce 1#{list_id}")
                return

        elif cmd == "move":
            if not list_id:
                await message.respond("sauce move 1#1 2")
                return
            else:
                await message.respond(f"sauce move 1#{list_id} 2")
                return

        elif cmd == "delete" or cmd == "del" or cmd == "delet":
            if not list_id:
                await message.respond("sauce delete 1#1")
                return
            else:
                await message.respond(f"sauce delete 1#{list_id}")
                return

    elif prefix == "st":
        if not cmd:
            if not list_id:
                await message.respond("sauce 2#1")
                return
            else:
                await message.respond(f"sauce 2#{list_id}")
                return

        elif cmd == "move":
            if not list_id:
                await message.respond("sauce move 2#1 3")
                return
            else:
                await message.respond(f"sauce move 2#{list_id} 3")
                return

        elif cmd == "delete" or cmd == "del" or cmd == "delet":
            if not list_id:
                await message.respond("sauce delete 2#1")
                return
            else:
                await message.respond(f"sauce delete 2#{list_id}")
                return

    elif prefix == "lc":
        if not cmd:
            if not list_id:
                await message.respond("sauce lc 3#1")
                return
            else:
                await message.respond(f"sauce lc 3#{list_id}")
                return

        elif cmd == "move":
            if not list_id:
                await message.respond("sauce move 3#1 4")
                return
            else:
                await message.respond(f"sauce move 3#{list_id} 4")
                return

        elif cmd == "delete" or cmd == "del" or cmd == "delet":
            if not list_id:
                await message.respond("sauce delete 3#1")
                return
            else:
                await message.respond(f"sauce delete 3#{list_id}")
                return

        elif cmd == "help":
            app_data = await bot.rest.fetch_application()
            embed = hikari.Embed(
                title="Commands",
                color=hikari.Color.from_rgb(171, 110, 71),
                timestamp=datetime.now(timezone.utc),
            )
            embed.add_field(
                name="QC shortcuts",
                value="`qc [id]`: equivalent to `sauce 1#[id]` (defaults to 1#1).\n\n"
                "`qc move [id]`: equivalent to `sauce move 1#[id] 2` (defaults to 1#1).\n\n"
                "`qc del/delete/delet [id]`: equivalent to `sauce delete 1#[id]` (defaults to 1#1).\n\n",
                inline=True,
            )
            embed.add_field(
                name="Sorting shortcuts",
                value="`st [id]`: equivalent to `sauce 2#[id]` (defaults to 2#1).\n\n"
                "`st move [id]`: equivalent to `sauce move 2#[id] 3` (defaults to 2#1).\n\n"
                "`st del/delete/delet [id]`: equivalent to `sauce delete 2#[id]` (defaults to 2#1).\n\n",
                inline=True,
            )
            embed.add_field(
                name="LC shortcuts",
                value="`lc`: equivalent to `sauce lc 3#[id]` (defaults to 3#1).\n\n"
                "`lc move`: equivalent to `sauce move 3#[id] 4` (defaults to 3#1).\n\n"
                "`lc del/delete/delet [id]`: equivalent to `sauce delete 3#[id]` (defaults to 3#1).\n\n"
                "`lc retry`: repeats Sriracha's last `.lc` command in the channel. Use if License Checker freezes on a search.\n\n"
                "`lc help` : this.\n\n"
                "`[en | jp]`: reacts with 🇺🇸 or 🇯🇵 to the last Sriracha message in the channel.\n\n",
                inline=True,
            )
            embed.set_author(
                name="LC streamliner",
                icon=bot.get_me().avatar_url
            )
            embed.set_footer(
                text="Made by Plurmp McFlurnten#7538",
                icon=app_data.owner.avatar_url
            )
            embed.set_thumbnail(
                bot.get_me().avatar_url
            )
            await message.respond(embed=embed)
            return

    elif prefix == "en":
        try:
            await last_sriracha_embed[message_event.get_channel().name].remove_reaction("🇺🇸")
        except NotFoundError:
            pass
        await last_sriracha_embed[message_event.get_channel().name].add_reaction("🇺🇸")

    elif prefix == "jp":
        try:
            await last_sriracha_embed[message_event.get_channel().name].remove_reaction("🇯🇵")
        except NotFoundError:
            pass
        await last_sriracha_embed[message_event.get_channel().name].add_reaction("🇯🇵")


bot.run(
    activity=Activity(name="Sriracha | lc help", type=ActivityType.WATCHING)
)
