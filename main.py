import BOT_setup
import copy
import json
import os
import aiofiles
from discord.ext import commands, tasks
import discord

import bot_clan_members
import clan_invite_embed
import sys
from os import environ

import openai
from chat_gpt.ask_gpt import init_gpt, hello_gpt
from chat_gpt import ask_gpt
from evidenta_populatiei.beginner_db import populate_db

from sherpa import functions_sherpa
from sherpa.sherpa_channel import sherpa_refresher
from sherpa import create_sherpa, sherpa_channel

from organizari_bot import functions
from organizari_bot.org_channel import org_refresher
from organizari_bot import create_org, org_channel

from utilities import donator_manage, donator_automod
from help.help_embed import init_help
from audit_log import audit_builder
from utilities.donator_automod import booster_manage

class UtilsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)  # se apeleaza la @
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or('/test'))
        # sau cand e comanda cu $
        self.synced = False

    # async def setup_hook(self, view) -> None:
    #     self.add_view(view)

    async def on_ready(self):
        command_tree.add_command(sherpa_command)
        command_tree.add_command(org_command)

        if not self.synced:
            await command_tree.sync(guild=discord.Object(id=BOT_setup.GUILD_ID))
            self.synced = True

        # cmd_channel = await bot.fetch_channel(797387549089333268)
        # await cmd_channel.send(content='Bot online — Kind reminder sa restartezi embedul cu link-uri')

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        print('Starting tasks...')

        if not (test_bot):
            do_refresh_db.start()
            do_refresh_embed.start()
            do_refresh_bot.start()
            do_refresh_donator.start()
            # do_refresh_leaderboard.start()
            post_refresher.start()
            organizare_refresher.start()
        else:
            print('—— Bot de teste')
            do_refresh_db.start()
            organizare_refresher.start()


        print('Done!')
        print('------')
        print('Refreshing orgs')
        with open("./chat_gpt/api_key.txt", "r") as f:
            openai.api_key = f.read().strip('\n')
        discord.utils.setup_logging()

        async def main():
            await sherpa_refresher(bot, BOT_setup.ORG_CHANNEL)
            await org_refresher(bot, BOT_setup.ORG_CHANNEL)

        if __name__ == "__main__":
            await main()
        print('Done!')
        print('------')
        print('Bot ready!')
        print('------')


sherpa_command = discord.app_commands.Group(name='sherpa', description='Optiuni organizari sherpa de tip SHERPA.',
                                            guild_ids=[BOT_setup.GUILD_ID])
org_command = discord.app_commands.Group(name='organizare', description='Optiuni pentru organizari.',
                                         guild_ids=[BOT_setup.GUILD_ID])
bot = UtilsBot()
command_tree = bot.tree  # discord.app_commands.CommandTree(bot)


'''
pentru event
'''
event_processing = False
event_last_user = None

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Comenzi management
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


@command_tree.command(name='curatenie_generala', description='Admin-only',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def privat_1(interaction: discord.Interaction, role_call: discord.Role):
    print(f'{"—" * 10} \nInitializare curatenie pentru {role_call.name} ')
    await bot_clan_members.init(bot, role_call, interaction)


@command_tree.command(name='generate_clan_invite_embed', description='Admin-only',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def privat_2(interaction: discord.Interaction):
    print(f'{"—" * 10} \nGenerare embed cu invinte link')
    await clan_invite_embed.init(interaction, bot)



@command_tree.command(name='fix_uhenp', description='Uhenp-only', guild=discord.Object(id=BOT_setup.GUILD_ID))
async def privat_69(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = await bot.fetch_guild(BOT_setup.GUILD_ID)
    uhenp_nou = await guild.fetch_member(1084179145510105138)
    uhenp_vechi = await guild.fetch_member(576077948168437760)
    for role in uhenp_nou.roles:
        if role not in uhenp_vechi.roles:
            await uhenp_vechi.add_roles(role)
    await interaction.followup.send(content='Fixed Uhenp')


@command_tree.command(name='help_d2ro', description='Meniu help D2 RO', guild=discord.Object(id=BOT_setup.GUILD_ID))
async def privat_70(interaction: discord.Interaction):
    await init_help(interaction, bot)


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Event-uri
—————————————————————————————————————————————————————————————————————————————————————————————————

'''

# @command_tree.command(name='dayone_register', description='Inscrie echipa pentru Day One — Lightfall',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
# async def privat_3(interaction:discord.Interaction, membru_2: discord.User, membru_3: discord.User,
#                    membru_4: discord.User, membru_5: discord.User, membru_6: discord.User):
#     print(f'{"—"*10} \nGenerare embed register day one team')
#     cmd_channel = await bot.fetch_channel(797387549089333268)
#
#     author = interaction.user
#     args = [author, membru_2, membru_3, membru_4, membru_5, membru_6]
#     # await interaction.response.defer()
#     await interaction.response.send_message(content='Asteapta, te rog.', ephemeral=True)
#     await bot_register_dayone.init(cmd_channel, args)


# @command_tree.command(name='event_register', description='Inscrie pentru competitia de speedrun — Lightfall',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
# async def privat_4(interaction:discord.Interaction, link: str):
#     print(f'{"—"*10} Inscriere noua pentru competitie {interaction.user.nick if interaction.user.nick else interaction.user.name}')
#     global event_processing, event_last_user
#
#     author = interaction.user
#
#     if event_processing and event_last_user != author.id:
#         await interaction.response.send_message(content="Momentan comanda este folosita de alt utilizator, te rog sa revi in cateva momente.",ephemeral=True)
#         return
#     event_processing = True
#     event_last_user = author.id
#
#     author_name = author.nick
#     if not author_name:
#         author_name = author.name
#
#     cmd_channel = await bot.fetch_channel(1075893874754588722)
#
#     # await interaction.response.defer()
#     # await interaction.response.send_message(content='Asteapta, te rog.', ephemeral=True)
#     try:
#         await register_concurs.init(interaction, author_name, link, cmd_channel)
#     finally:
#         event_processing = False


# @command_tree.command(name='build_leaderboard', description='Setup leaderboard',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
# async def privat_5(interaction:discord.Interaction):
#     print(f'{"—"*10} Initializare leaderboard competitie')
#     cmd_channel = await bot.fetch_channel(1075884178731700355)
#
#     await interaction.response.send_message(content='Se trimite cand e', ephemeral=False)
#     dest_api = bungie_api.DestinyAPI()
#     await build_leaderboard.init(cmd_channel, dest_api)


# @tasks.loop(minutes=51)
# async def do_refresh_leaderboard():
#     import datetime
#     if datetime.datetime.now() < datetime.datetime(2023,2,26,18,0,0):
#         print(f'{"—" * 5} Refresh leaderboard clan link {"—" * 5}')
#         leaderboard_channel = await bot.fetch_channel(1075884178731700355)
#         dest_api = bungie_api.DestinyAPI()
#         await build_leaderboard.refresh_leaderboar(leaderboard_channel, dest_api)

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Donator - Vet
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


@command_tree.command(name='transfer', description='Poti sa dai join pe un canal voce peste limita',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def transfer_to_channel(interaction: discord.Interaction, canal_voce: discord.VoiceChannel):
    print(
        f'{"—" * 10} Initializare transfer {interaction.user.nick if interaction.user.nick else interaction.user.name}')

    try:
        voice_channel = canal_voce
        author = interaction.user
        updates_channel = await bot.fetch_channel(BOT_setup.PLAYER_UPDATES_CHANNEL)

        if str(BOT_setup.VIP_ROLE) in str(author.roles):
            transfer_str = f'Transfer VIP {author.mention} pe canalul voce **{voice_channel.name}**'
        elif str(BOT_setup.DONATOR_ROLE) in str(author.roles):
            transfer_str = f'Transfer Donator {author.mention} pe canalul voce **{voice_channel.name}**'
        elif str(BOT_setup.SERVER_BOOSTER) in str(author.roles):
            transfer_str = f'Transfer Booster {author.mention} pe canalul voce **{voice_channel.name}**'
        else:
            transfer_str = f'Transfer {author.mention} pe canalul voce **{voice_channel.name}**'

        await author.move_to(voice_channel)
        await updates_channel.send(content=transfer_str)
        await interaction.response.send_message(content=transfer_str)
    except:
        await interaction.response.send_message(content=f'Intra pe un canal voce pentru a putea fi transferat',
                                                ephemeral=True)


@command_tree.command(name='donator_check', description='Vezi donatori peste limita',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def detect_no_donate(interaction: discord.Interaction):
    print(f'{"—" * 10} Initializare detect not donator')

    await donator_manage.init(bot, interaction)


@command_tree.command(name='donator_add', description='Adauga donator cu limita de timp',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def add_new_ddonator(interaction: discord.Interaction, membru: discord.Member, an: str, luna: str, zi: str):
    print(f'{"—" * 10} Initializare adauga donator {membru.display_name}')

    timp = f'{zi}/{luna}/{an}'

    await donator_manage.add_donator(interaction, bot, membru, timp)


@command_tree.command(name='lock_channel', description='Limitare acces canal voce actual',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def lock_for_donator(interaction: discord.Interaction, limita_user:int = 0):
    updates_channel = await bot.fetch_channel(BOT_setup.PLAYER_UPDATES_CHANNEL)
    author = interaction.user

    if limita_user > 10:
        await interaction.response.send_message(content='Limita maxima este 10!', ephemeral=True)
        return

    try:
        voice_channel = author.voice.channel
    except:
        await interaction.response.send_message(content='Trebuie sa intri intr-un canal voce.', ephemeral=True)
        return

    if 'Tower' in voice_channel.name:
        await interaction.response.send_message(content='Nu poti restrange un canal __**Tower**__', ephemeral=True)
        return

    print(f'{"—" * 10} Inchidere canal {voice_channel.name} de catre {author.nick if author.nick else author.name}')

    try:
        if limita_user:
            new_limit = limita_user
        else:
            new_limit = len(voice_channel.members)
        await voice_channel.edit(user_limit=new_limit)

        await interaction.response.send_message(content=f'Restrangere canal voce __**{voice_channel.name}**__ de catre {author.mention}')
        await updates_channel.send(content=f'Restrangere canal voce __**{voice_channel.name}**__ de catre {author.mention}')
    except:
        await interaction.response.send_message(content='Trebuie sa intri intr-un canal voce.', ephemeral=True)


@tasks.loop(minutes=30)
async def do_refresh_donator():
    from datetime import datetime
    now = datetime.now()
    date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f'[{date_time_string}] {"—" * 2} Refresh lista donatori {"—" * 5}')
    await donator_automod.init(bot)


@bot.event
async def on_member_update(before:discord.Member, after:discord.Member):
    await booster_manage(before, after, bot)

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Organizari - Sherpa
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


# @command_tree.command(name='sherpa_create', description='Creaza o noua organizare de Sherpa.',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
@sherpa_command.command(name='create', description='Creaza o noua organizare de Sherpa.')
async def create_rog(interaction: discord.Interaction):
    print(f'{"—" * 10} \nInitializare creare ')
    await create_sherpa.create(interaction, bot, interaction.user)


# @command_tree.command(name='sherpa_edit', description='Editeaza o organizare de Sherpa existenta.',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
@sherpa_command.command(name='edit', description='Editeaza o organizare de Sherpa.')
async def edit_rog(interaction: discord.Interaction, id: str):
    print(f'{"—" * 10} \nInitializare edit ')
    await create_sherpa.edit(interaction, bot, interaction.user, id)


@tasks.loop(minutes=1)
async def post_refresher():
    reminder_id = BOT_setup.REMINDER_CHANNEL  # 1078798703902597252

    with open('sherpa/org_sherpa.json', 'r') as f:
        org_dict = json.load(f)["org"]

    if not org_dict:
        return

    for org in org_dict:
        _org = copy.deepcopy(org)
        from datetime import datetime

        print(org['ID'])

        # Assuming your epoch time is stored in a variable named 'epoch_time'
        epoch_time = int(org['Datetime'])

        # Convert the epoch time to a datetime object and localize it to Bucharest timezone
        user_datetime = datetime.fromtimestamp(epoch_time)

        # Calculate the minute_difference between the current time and the event's server datetime
        current_server_time = datetime.now()
        time_difference = user_datetime - current_server_time
        minute_difference = int(time_difference.total_seconds() / 60)

        if minute_difference < 60 and org['Org_info']['Reminder'] == 0:
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions_sherpa.make_reminder_string(org, 'A', 'o ora')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 1
            functions_sherpa.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 30 and org['Org_info']['Reminder'] == 1:
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions_sherpa.make_reminder_string(org, 'Au', '30 min')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 2
            functions_sherpa.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 15 and org['Org_info']['Reminder'] == 2:
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions_sherpa.make_reminder_string(org, 'Au', '15 min')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 3
            functions_sherpa.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 0 and org['Org_info']['Reminder'] == 3 and org['Org_info']['Active'] == True:
            org['Org_info']['Active'] = False
            functions_sherpa.data_updater(org_old=_org, org_new=org)
            _org_channel = await bot.fetch_channel(BOT_setup.ORG_CHANNEL)
            message = await _org_channel.fetch_message(org['Message_id'])
            await sherpa_channel.edit_mesaj(bot, message, org, True)

        if minute_difference < -240 and org['Org_info']['Active'] is False:
            _org_channel = await bot.fetch_channel(BOT_setup.ORG_CHANNEL)
            message = await _org_channel.fetch_message(org['Message_id'])

            guild = await bot.fetch_guild(BOT_setup.GUILD_ID)
            sherpa_role = guild.get_role(org['Org_utils']['Sherpa'])
            org_role = guild.get_role(org['Org_utils']['Part'])
            sherpa_voice = await bot.fetch_channel(org['Org_utils']['Voice'])

            await sherpa_voice.delete()
            await sherpa_role.delete()
            await org_role.delete()
            await message.delete()

            functions_sherpa.data_updater(org_old=_org, org_new={})



'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Organizari - Normal
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


@org_command.command(name='create', description='Creaza o noua organizare.')
async def create_organizare(interaction: discord.Interaction):
    print(f'{"—" * 10} \nInitializare creare ')
    await create_org.create(interaction, bot, interaction.user)


@org_command.command(name='edit', description='Editeaza o organizare.')
async def edit_organizare(interaction: discord.Interaction, id: str):
    print(f'{"—" * 10} \nInitializare edit ')
    await create_org.edit(interaction, bot, interaction.user, id)


@tasks.loop(minutes=1)
async def organizare_refresher():
    reminder_id = BOT_setup.REMINDER_CHANNEL  # 1078798703902597252

    with open('organizari_bot/organizari.json', 'r') as f:
        org_dict = json.load(f)["org"]

    if not org_dict:
        return

    for org in org_dict:
        _org = copy.deepcopy(org)
        from datetime import datetime

        # Assuming your epoch time is stored in a variable named 'epoch_time'
        epoch_time = int(org['Datetime'])

        # Convert the epoch time to a datetime object and localize it to Bucharest timezone
        user_datetime = datetime.fromtimestamp(epoch_time)

        # Calculate the minute_difference between the current time and the event's server datetime
        current_server_time = datetime.now()
        time_difference = user_datetime - current_server_time
        minute_difference = int(time_difference.total_seconds() / 60)

        if 299 < minute_difference < 301:
            print(f'--- Schimb format org {org["ID"]}')
            _org_channel = await bot.fetch_channel(BOT_setup.ORG_CHANNEL)
            message = await _org_channel.fetch_message(org['Message_id'])
            await org_channel.edit_mesaj(bot, message, org)

        if minute_difference < 60 and org['Org_info']['Reminder'] == 0:
            print(f'--- reminder 1h org {org["ID"]}')
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions.make_reminder_string(org, 'A', 'o ora')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 1
            functions.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 30 and org['Org_info']['Reminder'] == 1:
            print(f'--- reminder 30min org {org["ID"]}')
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions.make_reminder_string(org, 'Au', '30 min')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 2
            functions.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 15 and org['Org_info']['Reminder'] == 2:
            print(f'--- reminder 15min org {org["ID"]}')
            reminder_channel = await bot.fetch_channel(reminder_id)
            reminder_string = functions.make_reminder_string(org, 'Au', '15 min')
            await reminder_channel.send(content=reminder_string)
            org['Org_info']['Reminder'] = 3
            functions.data_updater(org_old=_org, org_new=org)

        elif minute_difference < 0 and org['Org_info']['Active'] == True:  # and org['Org_info']['Reminder'] == 3 and org['Org_info']['Active'] == True:
            print(f'--- activare org {org["ID"]}')
            org['Org_info']['Active'] = False
            functions.data_updater(org_old=_org, org_new=org)
            _org_channel = await bot.fetch_channel(BOT_setup.ORG_CHANNEL)
            message = await _org_channel.fetch_message(org['Message_id'])
            await org_channel.edit_mesaj(bot, message, org, True)

        if minute_difference < -60 and org['Org_info']['Active'] is False:
            print(f'--- stergere org {org["ID"]}')
            _org_channel = await bot.fetch_channel(BOT_setup.ORG_CHANNEL)
            message = await _org_channel.fetch_message(org['Message_id'])

            guild = await bot.fetch_guild(BOT_setup.GUILD_ID)
            org_role = guild.get_role(org['Org_utils']['Part'])

            await org_role.delete()
            await message.delete()

            functions.data_updater(org_old=_org, org_new={})


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Bot events si task-uri 
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


@bot.event
async def on_member_join(member):
    if test_bot:
        return
    from datetime import datetime
    now = datetime.now()
    date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{date_time_string}] {'—' * 2} Generare mesaj membru nou - {member.name} {'—' * 5}")
    welcome_channel = await bot.fetch_channel(BOT_setup.WELCOME_CHANNEL)
    welcome_txt = '''Salut {name} ! Daca joci Destiny 2, o sa fie nevoie sa-ti dai register pentru a vedea canalele aferente jocului.
Pentru a-ti da register te rog sa mergi pe <#1101677816577273856> si sa apelezi comanda `/register` si sa urmezi pasii din mesajul primit.
Daca vrei sa te alturi unuia din clanurile noastre, pe <#{CLAN_INVITE_CHANNEL}> gasesti informatiile necesare.
Dacă întâmpini greutăți pe parcursul procesului, îți recomandăm să vorbești cu ChatBro, un bot de discuții inteligent, în thread-ul de mai jos. Mulțumim! '''

    new_message = await welcome_channel.send(content=welcome_txt.format(name=member.mention,
                                                                        CLAN_INVITE_CHANNEL=BOT_setup.CLAN_INVITE_CHANNEL))
    new_thread = await new_message.create_thread(name=f'Support Thread - {member.name}', auto_archive_duration=1440)

    try:
        with open('./chat_gpt/threads_ids.txt', 'a') as f:
            f.write(f'{new_thread.id} , ')

        with open('./chat_gpt/init_chat.json', 'r') as f:
            message_history = json.load(f)

        format_content = message_history["msg"][0]["content"].format(nume=member.mention)
        message_history["msg"][0]["content"] = format_content
        response = await init_gpt(message_history['msg'])
        gpt_response = response[-1]['content']

        await new_thread.send(content=gpt_response)

        message_history['msg'] = response
        with open(rf'./chat_gpt/threads/{new_thread.id}.json', 'w') as f:
            json.dump(message_history, f)

    except:
        await new_thread.send(
            content=f'Dacă întâmpini probleme, te rog să ne lași un mesaj aici și te vom asista în cel mai scurt timp posibil. {member.mention} <@&1104377935009419385>')


@tasks.loop(minutes=60)
async def do_refresh_embed():
    """
    Refresh automat la embed odata la 30 min
    Se reapeleaza Bungie API si se reconstruieste embedul principal
    Se editeaza mesajul original daca mai este activ
    """
    from datetime import datetime
    now = datetime.now()
    date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f'[{date_time_string}] {"—" * 2} Refresh embed clan link {"—" * 5}')
    clan_invite_channel = await bot.fetch_channel(BOT_setup.CLAN_INVITE_CHANNEL)
    try:
        with open('embed_msg.txt') as f:
            msg_id = str(f.readline())
    except:
        print('[INIT] Nu exista log al embedului')
        return

    if not msg_id:
        print('[INIT] Nu exista message_id al embedului')
        return

    try:
        embed_message = await clan_invite_channel.fetch_message(msg_id)
    except:
        print('[INIT] Mesajul cu embed nu mai exista!')
        return
    clan_numbers = clan_invite_embed.get_clan_stats()
    await embed_message.edit(content='', embed=clan_invite_embed.ClanEmbed(clan_numbers))


@tasks.loop(minutes=2)
async def do_refresh_bot():
    import datetime
    now = datetime.datetime.now()
    log_time = now.strftime("%m/%d/%Y %H:%M:%S")
    # print(f'[{log_time}] Refresh BOT')


@tasks.loop(minutes=60)
async def do_refresh_db():
    print(f'{"—" * 5} Refresh DataBase')
    await populate_db(bot, BOT_setup.GUILD_ID)



@bot.event
async def on_member_remove(member):
    from datetime import datetime
    now = datetime.now()
    date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{date_time_string}] {'—' * 2} A iesit - {member.name} {'—' * 5}")
    update_channel = await bot.fetch_channel(BOT_setup.PLAYER_UPDATES_CHANNEL)
    text = ''
    member_name = f'{member.nick if member.nick else member.name}'
    for role in member.roles:
        if '1102244192043942059' in str(role.id):
            text = f'Membrul __**{member_name}**__ a iesit si facea parte din <@&1102244192043942059>'
        elif '1102244836872032256' in str(role.id):
            text = f'Membrul __**{member_name}**__ a iesit si facea parte din <@&1102244836872032256>'
        elif '1102244973363081286' in str(role.id):
            text = f'Membrul __**{member_name}**__ a iesit si facea parte din <@&1102244973363081286>'
    if not text:
        text = f'Membrul __**{member_name}**__ a iesit'

    new_message = await update_channel.send(content=f'{text}')


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Chat-Bro
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


@command_tree.command(name='support_gpt', description='Intreaba-l pe ChatBro',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def test_gpt_2(interaction: discord.Interaction):
    await interaction.response.defer()
    message = await interaction.followup.send(content='Vorbeste in thread.')
    message_id = message.id
    new_thread = await interaction.channel.create_thread(name=f'Support Thread - {interaction.user.name}',
                                                         auto_archive_duration=1440, message=message)

    with open('./chat_gpt/support_ids.txt', 'a') as f:
        f.write(f'{new_thread.id} , ')


@command_tree.command(name='test_gpt', description='Intreaba-l pe ChatBro',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def test_gpt_2(interaction: discord.Interaction):
    await interaction.response.defer()
    message = await interaction.followup.send(content='Vorbeste in thread.')
    message_id = message.id
    new_thread = await interaction.channel.create_thread(name=f'Support Thread - {interaction.user.name}',
                                                         auto_archive_duration=1440, message=message)

    with open('./chat_gpt/threads_ids.txt', 'a') as f:
        f.write(f'{new_thread.id} , ')


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.Thread):
        if message.author.id == 1100486789673791558:  # or
            return
        if message.author.id == 1101506405942448170:
            return

        async with aiofiles.open('./chat_gpt/ignore_ids.txt', 'r') as f:
            ignore_ids = await f.read()
        if str(message.channel.id) in ignore_ids:
            return

        async with aiofiles.open('./chat_gpt/threads_ids.txt', 'r') as f:
            thread_ids = await f.read()

        async with aiofiles.open('./chat_gpt/support_ids.txt', 'r') as f:
            support_ids = await f.read()

        if str(message.channel.id) in thread_ids:
            try:
                async with aiofiles.open(rf'./chat_gpt/threads/{message.channel.id}.json', 'r') as f:
                    message_history = json.loads(await f.read())
            except:
                async with aiofiles.open('./chat_gpt/init_chat.json', 'r') as f:
                    message_history = json.loads(await f.read())
                    format_content = message_history["msg"][0]["content"].format(nume=message.author.mention)
                    message_history["msg"][0]["content"] = format_content

            message_history["msg"].append({'role': 'user', 'content': message.content})

            async with message.channel.typing():
                response, tokens = await ask_gpt.ask_gpt(message_history['msg'])
                gpt_response = response[-1]['content']
                await message.reply(content=gpt_response)

            message_history['msg'] = response

            async with aiofiles.open(rf'./chat_gpt/threads/{message.channel.id}.json', 'w') as f:
                content = json.dumps(message_history, indent=4)
                await f.write(content)

            if tokens > 3500:
                print('—— Membru prea prost')
                with open('./chat_gpt/ignore_ids.txt', 'a') as f:
                    f.write(f'{message.channel.id} ,')
                thread_ids.replace(f'{message.channel.id} ,', '')
                with open('./chat_gpt/threads_ids.txt', 'w') as f:
                    f.write(thread_ids)
                os.remove(rf'./chat_gpt/threads/{message.channel.id}.json')
                await message.reply(
                    content="ChatBro a fost a intrat in concediu medical, problema ta va fi preluata de catre un admin <@&1104377935009419385>")
                # await message.channel.edit(archived=True, locked=True)
                return

        elif str(message.channel.id) in support_ids:
            try:
                async with aiofiles.open(rf'./chat_gpt/threads/{message.channel.id}.json', 'r') as f:
                    message_history = json.loads(await f.read())
            except:
                async with aiofiles.open('./chat_gpt/init_chat.json', 'r') as f:
                    message_history = json.loads(await f.read())
                    format_content = message_history["msg"][0]["content"].format(nume=message.author.mention)
                    message_history["msg"][0]["content"] = format_content

            message_history["msg"].append({'role': 'user', 'content': message.content})

            async with message.channel.typing():
                response, tokens = await ask_gpt.ask_gpt(message_history['msg'])
                gpt_response = response[-1]['content']
                await message.reply(content=gpt_response)

            message_history['msg'] = response

            async with aiofiles.open(rf'./chat_gpt/threads/{message.channel.id}.json', 'w') as f:
                if tokens < 3500:
                    content = json.dumps(message_history, indent=4)
                    await f.write(content)
                else:
                    _temp_list = message_history['msg']
                    del _temp_list[1:3]
                    message_history['msg'] = _temp_list
                    content = json.dumps(message_history, indent=4)
                    await f.write(content)
        else:
            return
    else:
        return


# @bot.event
# async def on_thread_update(before: discord.Thread, after: discord.Thread):
#     if before.locked is False and after.locked is True:
#         print(f'—— Eliminat fisier pentru {after.name}')
#         with open('./chat_gpt/threads_ids.txt', 'r') as f:
#             thread_ids = f.read()
#         thread_ids.replace(f'{after.id} ,', '')
#         with open('./chat_gpt/threads_ids.txt', 'w') as f:
#             f.write(thread_ids)
#         updates_channel = await bot.fetch_channel(BOT_setup.PLAYER_UPDATES_CHANNEL)
#         await updates_channel.send(content=f'Eliminat fisier pentru {after.mention}')
#         os.remove(rf'./chat_gpt/threads/{after.id}.json')
#     if before.archived is False and after.archived is True:
#         print(f'—— Eliminat fisier pentru {after.name}')
#         with open('./chat_gpt/threads_ids.txt', 'r') as f:
#             thread_ids = f.read()
#         thread_ids.replace(f'{after.id} ,', '')
#         with open('./chat_gpt/threads_ids.txt', 'w') as f:
#             f.write(thread_ids)
#         updates_channel = await bot.fetch_channel(BOT_setup.PLAYER_UPDATES_CHANNEL)
#         await updates_channel.send(content=f'Eliminat fisier pentru {after.mention}')
#         os.remove(rf'./chat_gpt/threads/{after.id}.json')


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Test
—————————————————————————————————————————————————————————————————————————————————————————————————

'''

# @bot.event
# async def on_interaction(interaction:discord.Interaction):
#     from organizari_bot.functions import get_org_by_msg_id
#     from organizari_bot.org_channel import button_functions
#
#     print(interaction.type)
#     if interaction.type != 'component':
#         return
#
#     message = await interaction.message.fetch()
#     if message.channel.id != 1101037441999179827:
#         return
#
#     try:
#         org_dict = get_org_by_msg_id(int(message.id))
#     except:
#         raise ValueError('Nu exista log pentru aceasta org')
#
#     await button_functions(interaction=interaction, label=interaction.data['custom_id'], org_dict=org_dict,
#                            guild=await bot.fetch_guild(BOT_setup.GUILD_ID), message=message)


@command_tree.command(name='test_db', description='Creaza o noua organizare de Sherpa.',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def test_db(interaction: discord.Interaction):
    await populate_db(bot, BOT_setup.GUILD_ID)


@command_tree.command(name='test_event', description='Creaza o noua organizare de Sherpa.',
                      guild=discord.Object(id=BOT_setup.GUILD_ID))
async def test_voice(interaction: discord.Interaction):
    await audit_builder.prepare_audit(bot, BOT_setup.GUILD_ID, BOT_setup.AUDIT_CHANNEL)


# @command_tree.command(name='test_locale', description='Creaza o noua organizare de Sherpa.',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
# async def test_locale(interaction: discord.Interaction):
#     view = discord.ui.View()
#     view.add_item(TimezoneSelect())
#     await interaction.response.send_message(content="Please select your timezone from the dropdown menu.", view=view)
#
#
# class TimezoneSelect(discord.ui.Select):
#     def __init__(self):
#         MAIN_EUROPEAN_TIMEZONES = [
#             "Europe/London",
#             "Europe/Dublin",
#             "Europe/Lisbon",
#             "Europe/Madrid",
#             "Europe/Paris",
#             "Europe/Amsterdam",
#             "Europe/Berlin",
#             "Europe/Rome",
#             "Europe/Copenhagen",
#             "Europe/Stockholm",
#             "Europe/Oslo",
#             "Europe/Helsinki",
#             "Europe/Athens",
#             "Europe/Istanbul",
#             "Europe/Moscow",
#         ]
#
#         options = [
#             discord.SelectOption(label=timezone, value=timezone)
#             for timezone in MAIN_EUROPEAN_TIMEZONES
#         ]
#         print(len(options))
#
#         super().__init__(placeholder="Select your timezone", min_values=1, max_values=1, options=options)
#
#     async def callback(self, interaction: discord.Interaction):
#         selected_timezone = self.values[0]
#         # Save the timezone for the user, e.g., in a database or a file
#         # For this example, we'll just print it
#         print(f"{interaction.user}: {selected_timezone}")
#         await interaction.response.send_message(f"Your timezone has been set to {selected_timezone}.", ephemeral=True)

#
# @command_tree.command(name='test_embed', description='Creaza o noua organizare de Sherpa.',
#                       guild=discord.Object(id=BOT_setup.GUILD_ID))
# async def test_embed(interaction: discord.Interaction):
#     print(f'{"—" * 10} \nInitializare creare ')
#     channel = await bot.fetch_channel(1100487208936423556)
#     await channel.send(embed=TestEmbed(), view=TestView())
#
# class TestEmbed(discord.Embed):
#     def __init__(self):
#         super().__init__(title=f"test",
#                          description=f'test',
#                          color=0x3d3223)
#
# class TestView(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#
#         button = TestButtons()
#         self.add_item(button)
#
#
# class TestButtons(discord.ui.Button):
#     def __init__(self):
#         super().__init__(label='Test', style=discord.ButtonStyle.danger)
#
#         async def click(interaction: discord.Interaction):
#             await interaction.response.defer()
#
#             channel = interaction.channel
#
#             await channel.send('Test')
#
#         self.callback = click
#
#
# class TestEmbed(discord.Embed):
#     def __init__(self):
#
#         self.set_author(name='KH Sherpa',
#                         url=r'https://destiny2.ro/',
#                         icon_url='https://cdn.discordapp.com/attachments/1086761501852958820/1086778406210895872/Karp_Disc.png')
#
#         attribute_list = [797118742198747146, 1049223783724109834, 0x0088ff,
#                           r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768506252558416/DSC.png',
#                           r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768517837234306/DSC_exp.png']
#
#         org_dict = {"ID": "8812", "Activity": "Raid", "Type": "Deep Stone Crypt", "Datetime": "1682432321",
#                     "Info": "Asta chiar se face + teste bot, sa aveti arme de DPS (Linear si Rockets cu perk-uri de dmg), Parasite / Lament",
#                     "Beginners": "2", "Message_id": 1087121633011040398,
#                     "Participants": {"Sherpa": ["Dan Diaconescu#8727", 489214493503520778],
#                                      "Beginners": [["Albert#7319\ud83c\udf7c", 441305325719650304]],
#                                      "Experts": [["SelectDenis09#1084", 667295895339139072],
#                                                  ["Flyingaxe#8778", 447762349466583043]],
#                                      "Reserve": [["PanTeraS#7407 \ud83c\udf7c", 319186530499428373]]},
#                     "Org_info": {"Active": True, "Reminder": 3}}
#
#         role_id, guide_id, hex_color, active_img, expired_img = attribute_list
#
#         for i in range(11):
#             self.add_field(name='',
#                            value='',
#                            inline=True)
#
#         super().__init__(title=f"{org_dict['Type']} — SHERPA",
#                          description=f'Canal ghid: <#{1046138519506137208}>',
#                          color=hex_color)
#
#         self.set_field_at(index=0,
#                           name='Info',
#                           value=org_dict['Info'],
#                           inline=True)
#
#         self.set_field_at(index=2,
#                           name='ID',
#                           value=org_dict['ID'],
#                           inline=True)
#
#         self.set_field_at(index=3,
#                           name='Data si ora [RO]',
#                           value=f"<t:{org_dict['Datetime']}:f>",
#                           inline=False)
#
#         self.set_field_at(index=4,
#                           name='‎',
#                           value='‎',
#                           inline=False)
#
#         '''
#         Tratare participanti
#
#         '''
#
#         participants = org_dict['Participants']
#
#         self.set_field_at(index=5,
#                           name='Sherpa',
#                           value=participants['Sherpa'][0],
#                           inline=True)
#
#         if participants['Beginners']:
#             beginner_list = '\n'.join([beg[0] for beg in participants['Beginners']])
#         else:
#             beginner_list = '-'
#
#         self.set_field_at(index=7,
#                           name=f'Incepatori (max {org_dict["Beginners"]})',
#                           value=beginner_list,
#                           inline=True)
#
#         if participants['Experts']:
#             expert_list = '\n'.join([exp[0] for exp in participants['Experts']])
#         else:
#             expert_list = '-'
#
#         self.set_field_at(index=8,
#                           name=f'Experimentati',
#                           value=expert_list,
#                           inline=True)
#
#         if participants['Reserve']:
#             reserve_list = '\n'.join([rez[0] for rez in participants['Reserve']])
#         else:
#             reserve_list = '-'
#
#         self.set_field_at(index=10,
#                           name=f'Rezerve',
#                           value=reserve_list,
#                           inline=True)
#
#         if org_dict['Org_info']['Active'] == False:
#             image_url = expired_img
#         else:
#             image_url = active_img
#
#         self.set_image(url=image_url)


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    RUN
—————————————————————————————————————————————————————————————————————————————————————————————————

'''

global test_bot
# TOKEN = str(environ.get('TOKEN'))  # sus la run dropdown file -> edit config -> enviroment variables -> TOKEN
global test_bot
if len(sys.argv) > 1:
    test_bot = False
    TOKEN = sys.argv[1]
    bot.run(TOKEN)
else:
    test_bot = True
    TOKEN = str(environ.get('TOKEN_TEST'))
    bot.run(TOKEN)
