import copy
import json

import discord
from discord.ext import commands, tasks

from organizari.functions import get_org_by_msg_id, data_updater

global activity_details, GUILD_ID, org_id
activity_details = {
    # attribute_list  =      role_id, guide_id, hex_color, active_img, expired_img
    "King's fall": [1075455824748621840, 1048983462125768745, 0xff2f00, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769004074512444/KF.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769009954918560/KF_exp.png'],
    'Deep Stone Crypt': [1075455824765394986, 1049223783724109834, 0x0088ff, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768506252558416/DSC.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768517837234306/DSC_exp.png'],
    'Garden of Salvation': [1075455824765394988, 1046140173102104639, 0x367800, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768906603085936/GOS.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768917114007682/GOS_exp.png'],
    'Last Wish': [1075455824765394990, 1048985076345606315, 0x08fc76, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769106734293092/LW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769117081640960/LW_exp.png'],
    'Vault of Glass': [1075455824765394984, 1046139331938631780, 0x005939, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769696134660106/VOG.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769702442893322/VOG_exp.png'],
    'Vow of the Disciple': [1075455824748621842, 1048950466807070783, 0x470902, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769776791138355/VOW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769782935781457/VOW_exp.png'],
    'Root Of Nightmares': [1101410490363686952, 1086338007763783740, 0x7e0599, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769471777144842/RON.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769479008133222/RON_exp.png'],
    'Spire of the Watcher': [1075455824731852844, 1051035874193842206, 0xb86a04, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769561363300402/SOTW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769583622463548/SOTW_exp.png'],
    'Duality': [1075455824731852846, 1049227955227873291, 0x8a002c, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768698578190336/DUAL.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768698578190336/DUAL.png'],
    'Grasp of Averice': [1075455824731852848, 1049229682794569788, 0x00e66f, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768831755718676/GOA.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086768835048255548/GOA_exp.png'],
    'Pit': [1075455824748621836, 1086770866454540309, 0x692f0e, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769206160261120/PIT.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769213286387802/PIT_exp.png'],
    'Prophecy': [1075455824748621834, 1086770644982698024, 0x7200c9, r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769302222405832/PROPH.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1086769310778785852/PROPH_exp.png'],
    'Shattered Throne': [1075455824748621838, 1086770644982698024, 0x113045, r'https://cdn.discordapp.com/attachments/1078798703902597252/1101179619379519538/ST.png', r'https://cdn.discordapp.com/attachments/1078798703902597252/1101179634973945907/ST_exp.png']
}

GUILD_ID = 1075455824643764314
org_id = 1101037441999179827

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Functii
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


def data_reader():
    with open('./organizari/org_sherpa.json', 'r') as f:
        _temp = json.load(f)
        return _temp


def data_logger(org_dict):
    with open('./organizari/org_sherpa.json', 'w') as f:
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


def time_flagger(date_string):
    from datetime import datetime
    date_object = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
    time_difference = datetime.now() - date_object
    return int(time_difference.total_seconds() / 60)


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
    with open('./organizari/org_sherpa.json', 'r') as f:
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
    sherpa_name = participants['Sherpa'][0]
    if participants['Beginners']:
        beginner_list = '\n'.join([f'{beg[0]}🍼' for beg in participants['Beginners']])
    else:
        beginner_list = '-'

    if participants['Experts']:
        expert_list = '\n'.join([exp[0] for exp in participants['Experts']])
    else:
        expert_list = '-'

    if participants['Reserve']:
        reserve_list = '\n'.join(
            [rez[0] if not await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
             participants['Reserve']])
        # reserve_list = '\n'.join([rez[0] for rez in participants['Reserve']])
    else:
        reserve_list = '-'


    await message.edit(content='Organizare noua de sherpa!', embed=OrgEmbed(org_dict, attribute_list, sherpa_name, beginner_list, expert_list, reserve_list),
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
    sherpa_name = participants['Sherpa'][0]
    if participants['Beginners']:
        beginner_list = '\n'.join([f'{beg[0]}🍼' for beg in participants['Beginners']])
    else:
        beginner_list = '-'

    if participants['Experts']:
        expert_list = '\n'.join([exp[0] for exp in participants['Experts']])
    else:
        expert_list = '-'

    if participants['Reserve']:
        reserve_list = '\n'.join(
            [rez[0] if await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
             participants['Reserve']])
        # reserve_list = '\n'.join([rez[0] for rez in participants['Reserve']])
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
    if not block:
        await message.edit(content='Organizare noua de sherpa!', embed=OrgEmbed(org_dict, attribute_list, sherpa_name, beginner_list, expert_list, reserve_list),
                           view=OrgView(org_dict, attribute_list, bot))
    else:
        await message.edit(content='Organizare de sherpa a inceput!', embed=OrgEmbed(org_dict, attribute_list, sherpa_name, beginner_list, expert_list, reserve_list),
                           view=None)


class OrgEmbed(discord.Embed):
    def __init__(self, org_dict, attribute_list, sherpa_name, beginner_list, expert_list, reserve_list):
        role_id, guide_id, hex_color, active_img, expired_img = attribute_list
        super().__init__(title=f"{org_dict['Type']} — SHERPA",
                         description=f'Canal ghid: <#{1046138519506137208}>',
                         color=hex_color)
        self.set_author(name='KH Sherpa',
                        url=r'https://destiny2.ro/',
                        icon_url='https://cdn.discordapp.com/attachments/1086761501852958820/1086778406210895872/Karp_Disc.png')

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

        self.add_field(name='Sherpa',
                       value=sherpa_name,  # participants['Sherpa'][0]
                       inline=True)

        self.add_field(name='‎',
                       value='‎',
                       inline=True)

        # if participants['Beginners']:
        #     beginner_list = '\n'.join([f'{beg[0]}🍼' for beg in participants['Beginners']])
        # else:
        #     beginner_list = '-'

        self.add_field(name=f'Incepatori (max {org_dict["Beginners"]})',
                       value=beginner_list,
                       inline=True)

        # if participants['Experts']:
        #     expert_list = '\n'.join([exp[0] for exp in participants['Experts']])
        # else:
        #     expert_list = '-'

        self.add_field(name=f'Experimentati',
                       value=expert_list,
                       inline=True)

        self.add_field(name='‎',
                       value='‎',
                       inline=True)

        # if participants['Reserve']:
        #     # reserve_list = '\n'.join(
        #     #     [rez[0] if not check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
        #     #      participants['Reserve']])
        #     reserve_list = '\n'.join([rez[0] for rez in participants['Reserve']])
        # else:
        #     reserve_list = '-'

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

        '''
        De pus:
        write dict to json la init 
        read json la fiecare callback buton
        fetch message la fiecare callback 
        orice modificare dict duce la write json
        '''
        # org_channel = await _bot.fetch_channel(1078798703902597252)

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
    print(f'{interaction.user.nick if interaction.user.nick else interaction.user.name} a incercat sa dea {label}')
    await interaction.response.defer()
    button_label = label
    org_old = copy.deepcopy(org_dict)
    sherpa_role = guild.get_role(org_dict['Org_utils']['Sherpa'])
    org_role = guild.get_role(org_dict['Org_utils']['Part'])
    sherpa_voice = await _bot.fetch_channel(org_dict['Org_utils']['Voice'])

    attribute_list = activity_details[org_dict['Type']]
    role_id, _, _, _, _ = attribute_list

    if button_label == 'delete':
        if org_dict['Participants']['Sherpa'][1] == interaction.user.id:
            _, message = await get_message(_bot=_bot, org_dict=org_dict)

            await sherpa_voice.delete()
            await sherpa_role.delete()
            await org_role.delete()
            await message.delete()

            data_updater(org_old=org_dict, org_new={})

            # with open('./organizari/org_sherpa.json', 'r') as f:
            #     _temp = json.load(f)
            # _temp = _temp['org']
            # for _org in _temp:
            #     if _org == org_dict:
            #         _temp.remove(_org)
            # new_dump = {'org': _temp}
            # with open('./organizari/org_sherpa.json', 'w') as f:
            #     json.dump(new_dump, f)

    if button_label == 'join':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        beginner_len = len(org_dict['Participants']['Beginners'])
        exp_len = len(org_dict['Participants']['Experts'])

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)

        if org_dict['Participants']['Sherpa'][1] == interaction.user.id:
            return

        if (beginner_len + exp_len) >= 5:
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

        if org_dict['Participants']['Sherpa'][1] == interaction.user.id:
            await interaction.followup.send(content="Nu poti sa iti schimbi rolul ca Sherpa!", ephemeral=True)
            return

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

        if org_dict['Participants']['Sherpa'][1] == interaction.user.id:
            await interaction.followup.send(content="Nu poti sa parasesti organizarea ca Sherpa!",
                                            ephemeral=True)
            return

        if player_data in org_dict['Participants']['Experts']:
            org_dict['Participants']['Experts'].remove(player_data)

        if player_data in org_dict['Participants']['Beginners']:
            org_dict['Participants']['Beginners'].remove(player_data)

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)
        await author.remove_roles(org_role)
        await edit_mesaj(_bot, message, org_dict=org_dict)

    data_updater(org_old=org_old, org_new=org_dict)