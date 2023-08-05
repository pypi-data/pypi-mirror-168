import asyncio
import fortnitepy
import json
from termcolor import colored
import os 
from fortnitepy.ext import commands
import aioconsole
from functools import partial
import FortniteAPIAsync
from typing import Optional
import aiohttp
from discord import Webhook
from discord.ext import commands as discord
import discord as disc
import requests
fortnite_api = FortniteAPIAsync.APIClient()

with open('Settings.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(colored("มีข้อผิดพลาดในไฟล์ใดไฟล์หนึ่งของบอท!(Settings.json) หากคุณมีปัญหาในการพยายามแก้ไขให้เข้าร่วมเซิร์ฟเวอร์สนับสนุนความไม่ลงรอยกันเพื่อขอความช่วยเหลือ - https://discord.gg/Xqm7DaSCES", "red"))

        exit(1)
with open(f"languages/{data['Account']['language'].lower()}.json") as f:
    try:
        lang = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(colored("มีข้อผิดพลาดในไฟล์ใดไฟล์หนึ่งของบอท!(selfbotpy) หากคุณมีปัญหาในการพยายามแก้ไขให้เข้าร่วมเซิร์ฟเวอร์สนับสนุนความไม่ลงรอยกันเพื่อขอความช่วยเหลือ - https://discord.gg/Xqm7DaSCES", "red"))

        exit(1)
server = None
if data['Discord']['Webhook'] == "":
    filename = 'device_auths.json'
else: 
    webhook = Webhook.from_url(data['Discord']['Webhook'], session=aiohttp.ClientSession())
    filename = 'device_auths.json'



def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(Email, details):
    existing = get_device_auth_details()
    existing[Email] = details


    with open(filename, 'w') as fp:
        json.dump(existing, fp)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in data['Control']['Give full access to']
    return commands.check(predicate)

async def get_authorization_code():
    while True:
        response = await aioconsole.ainput(lang['auth'].format(email=data['Account']['Email']))
        if "redirectUrl" in response:
            response = json.loads(response)
            if "?code" not in response["redirectUrl"]:
                print(colored(lang['auth_error'], "red"))
                continue
            code = response["redirectUrl"].split("?code=")[1]
            return code
        else:
            if "https://accounts.epicgames.com/fnauth" in response:
                if "?code" not in response:
                    print(colored(lang['auth_error'], "red"))
                    continue
                code = response.split("?code=")[1]
                return code
            else:
                code = response
                return code

device_auth_details = get_device_auth_details().get(data['Account']['Email'], {})
client = discord.Bot(
    command_prefix=data['Discord']['Prefix'],
    case_insensitive=True,
    intents=disc.Intents.all()
)

bot = commands.Bot(
    command_prefix=data['Account']['Prefix'],case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        Email=data['Account']['Email'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        authorization_code=get_authorization_code,
        **device_auth_details
    ),
    status=data['Party']['Status'],
    platform=fortnitepy.Platform(data['Party']['Platform']),
)

@bot.event
async def event_device_auth_generate(details, Email):
    store_device_auth_details(data['Account']['Email'], details)




@bot.event
async def event_ready():
    
    print(colored(lang['start_message'].format(bot_name=bot.user.display_name, bot_id=bot.user.id, bot_platform=(str((bot.platform))[9:]).lower().capitalize()), 'green'))
    if data['Discord']['Webhook'] == "":
        pass
    else:
        await webhook.send(lang['start_message'].format(bot_name=bot.user.display_name, bot_id=bot.user.id, bot_platform=(str((bot.platform))[9:]).lower().capitalize()), username = "terminal")
    member = bot.party.me
    

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['Party']['Cosmetics']['Skin']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['Party']['Cosmetics']['Backpack']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['Party']['Cosmetics']['Pickaxe']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_emote,
            asset=data['Party']['Cosmetics']['Emote']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['Party']['Cosmetics']['Banner']['Banner Name'],
            color=data['Party']['Cosmetics']['Banner']['Banner Color'],
            season_level=data['Party']['Cosmetics']['Banner']['Season Level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['Party']['Cosmetics']['Banner']['battle pass tier']
        )
    )
    if data['Discord']['Token'] == "":
        return
    else:
        await client.start(data['Discord']['Token'])
   

@bot.event
async def event_friend_message(message):
    if data['Discord']['Webhook'] == "":
        pass
    else: 
        await webhook.send(lang["whisper"].format(message=message.content), username = "Whisper Logs")
@bot.event
async def event_party_message(message):
    if data['Discord']['Webhook'] == "":
        pass
    else:
        await webhook.send(lang["party"].format(message=message.content), username = "Chat Logs")

@bot.event
async def event_friend_add(Friend):
    if not data['Control']['Public Bot']:
        if not Friend.id in data['Control']['Give full access to']:
            return
    
    try:
        await Friend.invite()
    except:
        pass




    

@bot.event
async def event_party_invite(invite):
    if data['Party']['Join party on invitation'].lower() == 'true':
        try:
            await invite.accept()
            print(colored(lang['accept_party'].format(sender=invite.sender.display_name), 'blue'))
        except Exception:
            pass
    elif data['Party']['Join party on invitation'].lower() == 'false':
        if invite.sender.id in data['Control']['Give full access to']:
            await invite.accept()
            print(colored(lang['accept_party'].format(sender=invite.sender.display_name), 'blue'))
        else:
            print(colored(lang['reject_party'].format(sender=invite.sender.display_name), 'red'))
def lenFriends():
    friends = bot.friends
    return len(friends)

def lenPartyMembers():
    members = bot.party.members
    return len(members)
    
@bot.event
async def event_party_member_promote(old_leader, new_leader):
    if new_leader.id == bot.user.id:
        await bot.party.send(lang['promo_old'].format(old_leader=old_leader.display_name))
        await bot.party.me.set_emote("EID_TrueLove")


@bot.event
async def event_friend_request(request):
    if data['Friends']['Accept all friend requests'].lower() == 'true':
        try:
            await request.accept()
            print(colored(lang['accept_friend'].format(request=request.display_name), 'blue'))
        
        except Exception:
            pass
    elif data['Friends']['Accept all friend requests'].lower() == 'false':
        if request.id in data['Control']['Give full access to']:
            try:
                await request.accept()
                print(colored(lang['accept_friend'].format(request=request.display_name), 'blue'))
            except Exception:
                pass
        else:
            print(colored(lang['reject_friend'].format(request=request.display_name), 'red'))
@bot.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(lang['command_notfound'].format(prefix=data['Account']['Prefix']))
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(lang['no_access'])
    elif isinstance(error, TimeoutError):
        await ctx.send(lang['your_slow'])
    else:
        print(error)


@bot.command()
@is_admin()
async def unhide(ctx, *,user = None) -> None:
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is False:
        await ctx.send(lang['already_unhidden'])
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=False)})
    await ctx.send(lang['unhidden_user'].format(member=member.display_name))


@bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(lang['emote_none'].format(prefix=data['Account']['Prefix']))
    elif content.lower() == 'floss':
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send(lang['emote_set'].format(cosmetic='Floss'))
    elif content.lower() == 'none':
        await bot.party.me.clear_emote()
        await ctx.send(lang['emote_set'].format(cosmetic='None'))
    elif content.upper().startswith('EID_'):
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset=content.upper())
        await ctx.send(lang['emote_set'].format(cosmetic=content))
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(lang['emote_set'].format(cosmetic=cosmetic.name))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(lang['emote_set'].format(cosmetic=content))


@bot.command()
@is_admin()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await bot.fetch_user(ctx.author.display_name)
        member = bot.party.get_member(user.id)
    else:
        user = await bot.fetch_user(epic_username)
        member = bot.party.get_member(user.id)

    if member is None:
        await ctx.send(lang['promo_notfound'])
    else:
        try:
            await member.promote()
            await ctx.send(lang['promo_user'].format(member=member.display_name))
            print(colored(lang['promo_user'].format(member=member.display_name), "blue"))
        except fortnitepy.errors.Forbidden:
            await ctx.send(lang['promo_forbidden'])
            print(colored(lang['promo_forbidden'], "blue"))


@bot.command()
@is_admin()
async def hide(ctx, *, user = None):
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is True:
        await ctx.send(lang['already_hidden'])
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=True)})
    await ctx.send(lang['hidden_user'].format(member=member.display_name))


@bot.command()
async def pinkghoul(ctx):
    variants = bot.party.me.create_variants(material=3)

    await bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send(lang['skin_set'].format(skin='Pink Ghoul Trooper'))


@bot.command()
async def purpleskull(ctx):
    variants = bot.party.me.create_variants(clothing_color=1)

    await bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send(lang['skin_set'].format(skin='Purple Skull Trooper'))





@bot.command()
async def goldpeely(ctx):
    variants = bot.party.me.create_variants(progressive=4)

    await bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send(lang['skin_set'].format(skin='Golden Peely'))


@bot.command()
async def hatlessrecon(ctx):
    variants = bot.party.me.create_variants(parts=2)

    await bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send(lang['skin_set'].format(skin='Hatless Recon Expert'))



@bot.command()
async def hologram(ctx):
    await bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send(lang['skin_set'].format(skin='Hologram'))






@bot.command()
async def ready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send(lang['ready'])



@bot.command()
async def unready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send(lang['unready'])



@bot.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(lang['skin_none'].format(prefix=data['Account']['Prefix']))
    elif content.upper().startswith('CID_'):
        await bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(lang['skinf_set'].format(cosmetic=content))
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(lang['skinf_set'].format(cosmetic=cosmetic.name))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(lang['skin_notfound'].format(cosmetic=content))


@bot.command()
async def sitin(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send(lang['sitin'])


@bot.command()
async def sitout(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send(lang['sitout'])


@bot.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(lang['tier_none'].format(prefix=data['Account']['Prefix'])) 
    else:
        await bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(lang['tier_set'].format(tier=tier))


@bot.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(lang['level_none'].format(prefix=data['Account']['Prefix']))
    else:
        await bot.party.me.set_banner(season_level=level)
        await ctx.send(lang['level_set'].format(level=level))
        
@bot.command()
async def crowns(ctx, amount=1, type=None):
    meta = bot.party.me.meta
    data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))[
        'AthenaCosmeticLoadout']
    try:
        data['cosmeticStats'][1]['statValue'] = int(amount)
    except KeyError:
        data['cosmeticStats'] = [
            {
                "statName": "TotalVictoryCrowns",
                "statValue": int(amount)
            },
            {
                "statName": "TotalRoyalRoyales",
                "statValue": int(amount)
            },
            {
                "statName": "HasCrown",
                "statValue": 0
            }
        ]
    final = {'AthenaCosmeticLoadout': data}
    key = 'Default:AthenaCosmeticLoadout_j'
    prop = {key: meta.set_prop(key, final)}

    await bot.party.me.patch(updated=prop)
    await bot.party.me.clear_emote()
    await asyncio.sleep(1)
    await bot.party.me.set_emote(asset='EID_Coronet')
    await ctx.send(lang['set_crowns'].format(crowns=amount))
    return


#discord

@client.command()
@commands.is_owner()
async def unhide(ctx, *,user = None) -> None:
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is False:
        await ctx.send(lang['already_unhidden'])
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=False)})
    await ctx.send(lang['unhidden_user'].format(member=member.display_name))


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(lang['emote_none'].format(prefix=data['Account']['Prefix']))
    elif content.lower() == 'floss':
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send(lang['emote_set'].format(cosmetic='Floss'))
    elif content.lower() == 'none':
        await bot.party.me.clear_emote()
        await ctx.send(lang['emote_set'].format(cosmetic='None'))
    elif content.upper().startswith('EID_'):
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset=content.upper())
        await ctx.send(lang['emote_set'].format(cosmetic=content))
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(lang['emote_set'].format(cosmetic=cosmetic.name))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(lang['emote_set'].format(cosmetic=content))


@client.command()
@commands.is_owner()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await bot.fetch_user(ctx.author.display_name)
        member = bot.party.get_member(user.id)
    else:
        user = await bot.fetch_user(epic_username)
        member = bot.party.get_member(user.id)

    if member is None:
        await ctx.send(lang['promo_notfound'])
    else:
        try:
            await member.promote()
            await ctx.send(lang['promo_user'].format(member=member.display_name))
            print(colored(lang['promo_user'].format(member=member.display_name), "blue"))
        except fortnitepy.errors.Forbidden:
            await ctx.send(lang['promo_forbidden'])
            print(colored(lang['promo_forbidden'], "blue"))


@client.command()
@commands.is_owner()
async def hide(ctx, *, user = None):
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is True:
        await ctx.send(lang['already_hidden'])
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=True)})
    await ctx.send(lang['hidden_user'].format(member=member.display_name))


@client.command()
async def pinkghoul(ctx):
    variants = bot.party.me.create_variants(material=3)

    await bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send(lang['skin_set'].format(skin='Pink Ghoul Trooper'))


@client.command()
async def purpleskull(ctx):
    variants = bot.party.me.create_variants(clothing_color=1)

    await bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send(lang['skin_set'].format(skin='Purple Skull Trooper'))





@client.command()
async def goldpeely(ctx):
    variants = bot.party.me.create_variants(progressive=4)

    await bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send(lang['skin_set'].format(skin='Golden Peely'))


@client.command()
async def hatlessrecon(ctx):
    variants = bot.party.me.create_variants(parts=2)

    await bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send(lang['skin_set'].format(skin='Hatless Recon Expert'))



@client.command()
async def hologram(ctx):
    await bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send(lang['skin_set'].format(skin='Hologram'))






@client.command()
async def ready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send(lang['ready'])



@client.command()
async def unready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send(lang['unready'])



@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(lang['skin_none'].format(prefix=data['Account']['Prefix']))
    elif content.upper().startswith('CID_'):
        await bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(lang['skinf_set'].format(cosmetic=content))
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(lang['skinf_set'].format(cosmetic=cosmetic.name))
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(lang['skin_notfound'].format(cosmetic=content))


@client.command()
async def sitin(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send(lang['sitin'])


@client.command()
async def sitout(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send(lang['sitout'])


@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(lang['tier_none'].format(prefix=data['Account']['Prefix'])) 
    else:
        await bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(lang['tier_set'].format(tier=tier))


@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(lang['level_none'].format(prefix=data['Account']['Prefix']))
    else:
        await bot.party.me.set_banner(season_level=level)
        await ctx.send(lang['level_set'].format(level=level))

@client.command()
async def crowns(ctx, amount=1, type=None):
    meta = bot.party.me.meta
    data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))[
        'AthenaCosmeticLoadout']
    try:
        data['cosmeticStats'][1]['statValue'] = int(amount)
    except KeyError:
        data['cosmeticStats'] = [
            {
                "statName": "TotalVictoryCrowns",
                "statValue": int(amount)
            },
            {
                "statName": "TotalRoyalRoyales",
                "statValue": int(amount)
            },
            {
                "statName": "HasCrown",
                "statValue": 0
            }
        ]
    final = {'AthenaCosmeticLoadout': data}
    key = 'Default:AthenaCosmeticLoadout_j'
    prop = {key: meta.set_prop(key, final)}

    await bot.party.me.patch(updated=prop)
    await bot.party.me.clear_emote()
    await asyncio.sleep(1)
    await bot.party.me.set_emote(asset='EID_Coronet')
    await ctx.send(lang['set_crowns'].format(crowns=amount))
    return


bot.run()