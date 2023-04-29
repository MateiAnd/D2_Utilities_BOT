import copy
import json

import discord
from discord.ext import commands

from organizari_bot.functions import get_org_by_msg_id, data_updater

global activity_details, GUILD_ID, org_id
activity_details = {
    # attribute_list  =      role_id, guide_id, hex_color, active_img, expired_img
    "King's fall": [1075455824748621840, 1048983462125768745, 0xff2f00, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830182496632912/KF.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830186653196388/KF_exp.png'],
    'Deep Stone Crypt': [1075455824765394986, 1049223783724109834, 0x0088ff, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830142550102126/DSC.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830143070187560/DSC_exp.png'],
    'Garden of Salvation': [1075455824765394988, 1046140173102104639, 0x367800, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830189773758524/GOS.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830181800390657/GOS_exp.png'],
    'Last Wish': [1075455824765394990, 1048985076345606315, 0x08fc76, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830187278151690/LW.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830187966005318/LW_exp.png'],
    'Vault of Glass': [1075455824765394984, 1046139331938631780, 0x005939, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830247806156830/VOG.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830248712122499/VOG_exp.png'],
    'Vow of the Disciple': [1075455824748621842, 1048950466807070783, 0x470902, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830249429352529/VOW.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830249974607914/VOW_exp.png'],
    'Root Of Nightmares': [1101410490363686952, 1086338007763783740, 0x7e0599, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830224104140861/RON.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830224653586562/RON_exp.png'],
    'Spire of the Watcher': [1075455824731852844, 1051035874193842206, 0xb86a04, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830225177882634/SOTW.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830225739907092/SOTW_exp.png'],
    'Duality': [1075455824731852846, 1049227955227873291, 0x8a002c, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830144034885742/DUAL.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830144374607922/DUAL_exp.png'],
    'Grasp of Averice': [1075455824731852848, 1049229682794569788, 0x00e66f, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830188431581315/GOA.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830189165576292/GOA_exp.png'],
    'Pit': [1075455824748621836, 1086770866454540309, 0x692f0e, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830206274158633/PIT.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830206773264465/PIT_exp.png'],
    'Prophecy': [1075455824748621834, 1086770644982698024, 0x7200c9, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830202381828096/PROPH.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830202776109116/PROPH_exp.png'],
    'Shattered Throne': [1075455824748621838, 1086770644982698024, 0x113045, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830247328002098/ST.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830246992461844/ST_exp.png'],
    'Crucible 6v6': [1075455824782184523, None, 0x9e0b1b, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830203451375747/PVP_6v6.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830204722262046/PVP_6v6_exp.png'],
    'Comp 3v3': [1075455824782184523, None,0x51050d, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830226478116894/PVP_comp.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830226935283753/PVP_comp_exp.png'],
    'Trials 3v3': [1075455824782184523, None, 0xe6b905, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830227296006296/PVP_trials.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830223739224105/PVP_trials_exp.png'],
    'Gambit': [1075455824782184523, None, 0x107b10, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830141052727316/GAMBIT.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830141455388743/GAMBIT_EXP.png'],
    'Nightfall': [1075455824782184523, None, 0x122258, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830205699522560/NF.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830205976358952/NF_exp.png'],
    'GM': [1075455824782184523, None, 0xb09b64, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830141811888148/GM.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101830142185189376/GM_exp.png'],
    'Defiant Battlegrounds': [1075455824782184523, None, 0x9f8ddf, r'https://cdn.discordapp.com/attachments/1100487208936423556/1101833349712068668/DBG.png', r'https://cdn.discordapp.com/attachments/1100487208936423556/1101833349032575087/DBG_exp.png']
}

GUILD_ID = 1075455824643764314
org_id = 1101037441999179827

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Functii
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


def data_reader():
    with open('./organizari_bot/organizari.json', 'r') as f:
        _temp = json.load(f)
        return _temp


def data_logger(org_dict):
    with open('./organizari_bot/organizari.json', 'w') as f:
        json.dump(org_dict, f)


def data_manager(org_dict, mode='a'):
    _temp = data_reader()
    if mode == 'a':
        _temp["org"].append(org_dict)
    elif mode == 'r':
        _temp["org"].remove(org_dict)
    elif mode == 'u':
        for org in _temp["org"]:
            if org['ID'] == org_dict['ID']:
                _temp["org"].remove(org)
                _temp["org"].append(org_dict)
    data_logger(_temp)


def get_org_by_id(_org_id: str):
    org_data = data_reader()['org']
    for org in org_data:
        if org["ID"] == _org_id:
            return org
    else:
        return {}


async def compare_users(interaction, author, user):
    if author == user:
        return 1
    else:
        await interaction.response.send_message(content='Caca nu e voie!', ephemeral=True)
        return 0


async def get_message(_bot, org_dict):
    org_channel = await _bot.fetch_channel(org_id)
    if not org_dict['Message_id']:
        message = await org_channel.send(content='temp')
        org_dict['Message_id'] = message.id
    else:
        message = await org_channel.fetch_message(org_dict['Message_id'])

    return org_dict, message


def random_int():
    from random import randint
    return int(''.join([str(randint(0, 9)) for i in range(10)]))


# def time_flagger(date_string):
#     from datetime import datetime
#     date_object = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
#     time_difference = datetime.now() - date_object
#     return int(time_difference.total_seconds() / 60)


def check_role(guild: discord.Guild, role_id, author):
    exp_role = guild.get_role(role_id)
    if exp_role in author.roles:
        return True
    return False


async def check_if_beginner(guild: discord.Guild, member_id, role_id) -> bool:
    member = await guild.fetch_member(int(member_id))
    eval = check_role(guild, role_id, member)
    return eval


async def org_refresher(bot, org_channel_id):
    with open('./organizari_bot/organizari.json', 'r') as f:
        _temp = json.load(f)

    orgs = _temp['org']
    if not orgs:
        return

    _org_channel = await bot.fetch_channel(org_channel_id)
    for org in orgs:
        message = await _org_channel.fetch_message(org['Message_id'])
        await edit_mesaj(bot, message, org)

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Creare mesaj
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def initializare_mesaj(bot: commands.Bot, org_dict):
    global _bot
    _bot = bot

    attribute_list = activity_details[org_dict['Type']]
    role_id, _, _, _, _ = attribute_list

    org_dict, message = await get_message(_bot, org_dict)
    data_manager(org_dict=org_dict, mode='a')
    guild = await bot.fetch_guild(GUILD_ID)

    participants = org_dict['Participants']
    author_name = participants['Author'][0]
    if participants['Beginners']:
        beginner_list = '\n'.join([f'{beg[0]}🍼' for beg in participants['Beginners']])
    else:
        beginner_list = '-'

    if participants['Experts']:
        expert_list = '\n'.join([f'{exp[0]} 👑' if exp[1] == participants['Author'][1] else exp[0] for exp in participants['Experts']])
    else:
        expert_list = '-'

    if participants['Reserve']:
        reserve_list = '\n'.join(
            [rez[0] if not await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
             participants['Reserve']])
    else:
        reserve_list = '-'


    await message.edit(content='Organizare noua!', embed=OrgEmbed(org_dict, attribute_list, author_name, beginner_list, expert_list, reserve_list),
                       view=OrgView(org_dict, attribute_list, bot))


async def init_edit(bot: commands.Bot, org_dict,):
    _, message = await get_message(bot, org_dict)
    data_manager(org_dict=org_dict, mode='u')
    await edit_mesaj(_bot, message, org_dict=org_dict)


async def edit_mesaj(bot: commands.Bot, message, org_dict, block=False):
    global _bot
    _bot = bot

    print('Initializare edit mesaj')
    attribute_list = activity_details[org_dict['Type']]
    role_id, _, _, _, _ = attribute_list
    guild = await bot.fetch_guild(GUILD_ID)

    participants = org_dict['Participants']
    author_name = participants['Author'][0]
    if participants['Beginners']:
        beginner_list = '\n'.join([f'{beg[0]}🍼' for beg in participants['Beginners']])
    else:
        beginner_list = '-'

    if participants['Experts']:
        expert_list = '\n'.join(
            [f'{exp[0]} 👑' if exp[1] == participants['Author'][1] else exp[0] for exp in participants['Experts']])
    else:
        expert_list = '-'

    if participants['Reserve']:
        reserve_list = '\n'.join(
            [rez[0] if await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
             participants['Reserve']])
    else:
        reserve_list = '-'

    # Problema la convert in cazul in care nu e epoch
    try:
        from datetime import datetime
        import pytz

        dt = datetime.strptime(org_dict['Datetime'], "%d/%m/%Y %H:%M")

        # Assume the datetime object is in Bucharest timezone
        bucharest_timezone = pytz.timezone("Europe/Bucharest")
        localized_datetime = bucharest_timezone.localize(dt)

        # Convert the localized datetime object to epoch time
        epoch_time = int(localized_datetime.timestamp())
        org_dict['Datetime'] = epoch_time
        print(org_dict['Datetime'])
    except:
        pass

    if org_dict['Org_info']['Active']:
        await message.edit(content='Organizare noua!', embed=OrgEmbed(org_dict, attribute_list, author_name, beginner_list, expert_list, reserve_list),
                           view=OrgView(org_dict, attribute_list, bot))
    else:
        await message.edit(content='Organizare a inceput!', embed=OrgEmbed(org_dict, attribute_list, author_name, beginner_list, expert_list, reserve_list),
                           view=None)


class OrgEmbed(discord.Embed):
    def __init__(self, org_dict, attribute_list, author_name, beginner_list, expert_list, reserve_list):
        role_id, guide_id, hex_color, active_img, expired_img = attribute_list
        super().__init__(title=f"Organizare — {org_dict['Type']}",
                         description=f'',
                         color=hex_color)
        self.set_author(name='D2-RO Scheduler',
                        url=r'https://destiny2.ro/',
                        icon_url='https://cdn.discordapp.com/attachments/1101368918318260274/1101498772560806001/logo_mic.png')

        self.add_field(name='ID',
                       value=org_dict['ID'],
                       inline=True)

        self.add_field(name='‎',
                       value='‎',
                       inline=True)

        self.add_field(name='Data si ora',
                       value=f"<t:{org_dict['Datetime']}:f>",
                       inline=True)

        self.add_field(name='Info',
                       value=org_dict['Info'],
                       inline=False)

        self.add_field(name='‎',
                       value='‎',
                       inline=False)

        '''
        Tratare participanti
        '''

        # participants = org_dict['Participants']
        if org_dict['Activity'] == 'Raid' or org_dict['Activity'] == 'Dungeon':

            if org_dict['Beginners'] != 0 or org_dict['Beginners'] is not None:
                beg_number = f"(max {org_dict['Beginners']} 🍼)"
            else:
                beg_number = "Fara 🍼"
            self.add_field(name=f'Participanti - {beg_number}',
                           value=f'{expert_list} \n {beginner_list}',
                           inline=True)

            self.add_field(name='‎',
                           value='‎',
                           inline=True)
        else:
            self.add_field(name=f'Participanti',
                           value=f'{expert_list} \n {beginner_list}',
                           inline=True)

            self.add_field(name='‎',
                           value='‎',
                           inline=True)


        # self.add_field(name=f'Incepatori (max {org_dict["Beginners"]})',
        #                value=beginner_list,
        #                inline=True)


        # self.add_field(name=f'Experimentati',
        #                value=expert_list,
        #                inline=True)

        # self.add_field(name='‎',
        #                value='‎',
        #                inline=True)


        self.add_field(name=f'Rezerve',
                       value=reserve_list,
                       inline=True)

        if org_dict['Org_info']['Active'] == False:
            image_url = expired_img
        else:
            image_url = active_img

        self.set_image(url=image_url)


class OrgView(discord.ui.View):
    def __init__(self, org_dict, attribute_list, bot):
        super().__init__(timeout=None)

        self.role_id = attribute_list[0]

        # Se initializeaza cu lista label butoane pentru First
        _lista_elemente = ['Join', 'Leave', 'Reserve', 'Delete']

        for elem in _lista_elemente:
            button = OrgButtons(bot, elem, self.role_id)
            self.add_item(button)


class OrgButtons(discord.ui.Button):
    def __init__(self, bot, button_label, role_id):
        self.button_lable = button_label
        self.role_id = str(role_id)

        if self.button_lable == 'Delete':
            super().__init__(label=self.button_lable, style=discord.ButtonStyle.danger, custom_id="delete")

        elif self.button_lable == 'Join':
            super().__init__(label=self.button_lable, style=discord.ButtonStyle.success, custom_id="join")

        elif self.button_lable == 'Reserve':
            super().__init__(label=self.button_lable, style=discord.ButtonStyle.secondary, custom_id="reserve")

        elif self.button_lable == 'Leave':
            super().__init__(label=self.button_lable, style=discord.ButtonStyle.danger, custom_id="leave")

        async def click(interaction: discord.Interaction):
            message = await interaction.message.fetch()
            try:
                org_dict = get_org_by_msg_id(int(message.id))
            except:
                raise ValueError('Nu exista log pentru aceasta org')

            await button_functions(interaction=interaction, label=interaction.data['custom_id'], org_dict=org_dict,
                                   guild=await bot.fetch_guild(GUILD_ID), message=message)

        self.callback = click


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Functii butoane
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def button_functions(interaction: discord.Interaction, label, org_dict, message, guild: discord.Guild):
    print(f'{interaction.user.nick if interaction.user.nick else interaction.user.name} a incercat sa dea {label} la org {org_dict["ID"]}')
    await interaction.response.defer()
    button_label = label
    org_old = copy.deepcopy(org_dict)
    org_role = guild.get_role(org_dict['Org_utils']['Part'])

    attribute_list = activity_details[org_dict['Type']]
    role_id, _, _, _, _ = attribute_list

    if button_label == 'delete':
        if org_dict['Participants']['Author'][1] == interaction.user.id:
            _, message = await get_message(_bot=_bot, org_dict=org_dict)

            await org_role.delete()
            await message.delete()

            data_updater(org_old=org_dict, org_new={})

    if button_label == 'join':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        max_players = org_dict['Max Number']
        beginner_len = len(org_dict['Participants']['Beginners'])
        exp_len = len(org_dict['Participants']['Experts'])

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)

        if (beginner_len + exp_len) >= max_players:
            if player_data not in org_dict['Participants']['Reserve']:
                org_dict['Participants']['Reserve'].append(player_data)
                await edit_mesaj(_bot, message, org_dict=org_dict)
                await author.add_roles(org_role)
            return

        if check_role(guild, role_id, author):
            if player_data not in org_dict['Participants']['Experts']:
                org_dict['Participants']['Experts'].append(player_data)
            else:
                return
            await author.add_roles(org_role)
            await edit_mesaj(_bot, message, org_dict=org_dict)
        else:
            if int(org_dict['Beginners']) <= beginner_len:
                await interaction.followup.send(content='Numarul maxim de inceptatori a fost atins!', ephemeral=True)
                if player_data not in org_dict['Participants']['Reserve']:
                    org_dict['Participants']['Reserve'].append(player_data)
                    await author.add_roles(org_role)
                    await edit_mesaj(_bot, message, org_dict=org_dict)
                return
            if player_data not in org_dict['Participants']['Beginners']:
                org_dict['Participants']['Beginners'].append(player_data)
                await author.add_roles(org_role)
                await edit_mesaj(_bot, message, org_dict=org_dict)
            else:
                return

    if button_label == 'reserve':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        if player_data in org_dict['Participants']['Experts']:
            org_dict['Participants']['Experts'].remove(player_data)

        if player_data in org_dict['Participants']['Beginners']:
            org_dict['Participants']['Beginners'].remove(player_data)

        if player_data not in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].append(player_data)
        await author.add_roles(org_role)
        await edit_mesaj(_bot, message, org_dict=org_dict)

    if button_label == 'leave':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        if player_data in org_dict['Participants']['Experts']:
            org_dict['Participants']['Experts'].remove(player_data)

        if player_data in org_dict['Participants']['Beginners']:
            org_dict['Participants']['Beginners'].remove(player_data)

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)
        await author.remove_roles(org_role)
        await edit_mesaj(_bot, message, org_dict=org_dict)

    data_updater(org_old=org_old, org_new=org_dict)
