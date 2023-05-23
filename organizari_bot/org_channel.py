import copy
import json

import discord
from discord.ext import commands
from copy import deepcopy
from organizari_bot.functions import get_org_by_msg_id, data_updater

global activity_details, GUILD_ID, org_id
# activity_details = {
#     # attribute_list  =      role_id, guide_id, hex_color, active_img, expired_img
#     "King's fall": [1075455824748621840, 1048983462125768745, 0xff2f00, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643580788551680/KF.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643580067123321/KF_exp.png'],
#     'Deep Stone Crypt': [1075455824765394986, 1049223783724109834, 0x0088ff, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643621263573103/DSC.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643621863379024/DSC_exp.png'],
#     'Garden of Salvation': [1075455824765394988, 1046140173102104639, 0x367800, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643664804663467/GOS.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643665412829305/GOS_exp.png'],
#     'Last Wish': [1075455824765394990, 1048985076345606315, 0x08fc76, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643696391950356/LW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643697063034970/LW_exp.png'],
#     'Vault of Glass': [1075455824765394984, 1046139331938631780, 0x005939, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643736980246580/VOG.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643737789730856/VOG_exp.png'],
#     'Vow of the Disciple': [1075455824748621842, 1048950466807070783, 0x470902, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643765744775299/VOW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643765300166686/VOW_exp.png'],
#     'Root Of Nightmares': [1101410490363686952, 1086338007763783740, 0x7e0599, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643806400167946/RON.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643806911868969/RON_exp.png'],
#     'Spire of the Watcher': [1075455824731852844, 1051035874193842206, 0xb86a04, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643862045995008/SOTW.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643861051936839/SOTW_exp.png'],
#     'Duality': [1075455824731852846, 1049227955227873291, 0x8a002c, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643890332381286/DUAL.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643889954898080/DUAL_exp.png'],
#     'Grasp of Averice': [1075455824731852848, 1049229682794569788, 0x00e66f, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643936717185166/GOA.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643936113197167/GOA_exp.png'],
#     'Pit': [1075455824748621836, 1086770866454540309, 0x692f0e, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643961660723220/PIT.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102643961153200178/PIT_exp.png'],
#     'Prophecy': [1075455824748621834, 1086770644982698024, 0x7200c9, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644001380773939/PROPH.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644001766645891/PROPH_exp.png'],
#     'Shattered Throne': [1075455824748621838, 1086770644982698024, 0x113045, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644025950994613/ST.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644025665794098/ST_exp.png'],
#     'Crucible 6v6': [1075455824782184523, None, 0x9e0b1b, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644065612353596/PVP_6v6.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644064672821258/PVP_6v6_exp.png'],
#     'Comp 3v3': [1075455824782184523, None,0x51050d, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644076345577512/PVP_comp.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644075959681044/PVP_comp_exp.png'],
#     'Trials 3v3': [1075455824782184523, None, 0xe6b905, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644099699462175/PVP_trials.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644099305181274/PVP_trials_exp.png'],
#     'Gambit': [1075455824782184523, None, 0x107b10, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644113209315390/GAMBIT.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644112810848297/GAMBIT_EXP.png'],
#     'Nightfall': [1075455824782184523, None, 0x122258, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644158570704997/NF.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644158285496400/NF_exp.png'],
#     'GM': [1075455824782184523, None, 0xb09b64, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644176799158402/GM.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644176543297586/GM_exp.png'],
#     'Defiant Battlegrounds': [1075455824782184523, None, 0x9f8ddf, r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644194490712237/DBG.png', r'https://cdn.discordapp.com/attachments/1086761501852958820/1102644193744130048/DBG_exp.png']
# }

activity_details = {
    # attribute_list  =      role_id, guide_id, hex_color, active_img, expired_img
    "King's fall": [1075455824748621840, 1048983462125768745, 0xff2f00, r'http://buzea.pro/buzea.pro/d2ro/Assets/KF.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/KF_exp.png'],
    'Deep Stone Crypt': [1075455824765394986, 1049223783724109834, 0x0088ff, r'http://buzea.pro/buzea.pro/d2ro/Assets/DSC.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/DSC_exp.png'],
    'Garden of Salvation': [1075455824765394988, 1046140173102104639, 0x367800, r'http://buzea.pro/buzea.pro/d2ro/Assets/GOS.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/GOS_exp.png'],
    'Last Wish': [1075455824765394990, 1048985076345606315, 0x08fc76, r'http://buzea.pro/buzea.pro/d2ro/Assets/LW.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/LW_exp.png'],
    'Vault of Glass': [1075455824765394984, 1046139331938631780, 0x005939, r'http://buzea.pro/buzea.pro/d2ro/Assets/VOG.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/VOG_exp.png'],
    'Vow of the Disciple': [1075455824748621842, 1048950466807070783, 0x470902, r'http://buzea.pro/buzea.pro/d2ro/Assets/VOW.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/VOW_exp.png'],
    'Root Of Nightmares': [1101410490363686952, 1086338007763783740, 0x7e0599, r'http://buzea.pro/buzea.pro/d2ro/Assets/RON.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/RON_exp.png'],
    'Spire of the Watcher': [1075455824731852844, 1051035874193842206, 0xb86a04, r'http://buzea.pro/buzea.pro/d2ro/Assets/SOTW.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/SOTW_exp.png'],
    'Duality': [1075455824731852846, 1049227955227873291, 0x8a002c, r'http://buzea.pro/buzea.pro/d2ro/Assets/DUAL.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/DUAL_exp.png'],
    'Grasp of Averice': [1075455824731852848, 1049229682794569788, 0x00e66f, r'http://buzea.pro/buzea.pro/d2ro/Assets/GOA.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/GOA_exp.png'],
    'Pit': [1075455824748621836, 1086770866454540309, 0x692f0e, r'http://buzea.pro/buzea.pro/d2ro/Assets/PIT.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PIT_exp.png'],
    'Prophecy': [1075455824748621834, 1086770644982698024, 0x7200c9, r'http://buzea.pro/buzea.pro/d2ro/Assets/PROPH.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PROPH_exp.png'],
    'Shattered Throne': [1075455824748621838, 1086770644982698024, 0x113045, r'http://buzea.pro/buzea.pro/d2ro/Assets/ST.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/ST_exp.png'],
    'Crucible 6v6': [1075455824782184523, None, 0x9e0b1b, r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6_exp.png'],
    'Comp 3v3': [1075455824782184523, None,0x51050d, r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp_exp.png'],
    'Trials 3v3': [1075455824782184523, None, 0xe6b905, r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials_exp.png'],
    'Gambit': [1075455824782184523, None, 0x107b10, r'http://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT_EXP.png'],
    'Nightfall': [1075455824782184523, None, 0x122258, r'http://buzea.pro/buzea.pro/d2ro/Assets/NF.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/NF_exp.png'],
    'GM': [1075455824782184523, None, 0xb09b64, r'http://buzea.pro/buzea.pro/d2ro/Assets/GM.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/GM_exp.png'],
    'Defiant Battlegrounds': [1075455824782184523, None, 0x9f8ddf, r'http://buzea.pro/buzea.pro/d2ro/Assets/DBG.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/DBG_exp.png']
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
    changes = None
    _temp = data_reader()
    if mode == 'a':
        _temp["org"].append(org_dict)
    elif mode == 'r':
        _temp["org"].remove(org_dict)
    elif mode == 'u':
        for org in _temp["org"]:
            if org['ID'] == org_dict['ID']:
                changes = get_changes(org, org_dict)
                print(f'--- Updated org {org["ID"]}')
                _temp["org"].remove(org)
                _temp["org"].append(org_dict)
    data_logger(_temp)
    if changes:
        return changes


def get_changes(org_old, org_new):
    changes = {}
    for key in org_old:
        if key == 'Org_info' or key == 'Editing' or key == 'Participants':
            continue
        if org_new[key] != org_old[key]:
            changes[key] = [org_new[key], org_old[key]]
    return changes


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
        print(org['ID'])
        message = await _org_channel.fetch_message(org['Message_id'])
        await edit_mesaj(bot, message, org)


async def create_part_stings(org_dict: dict, guild, role_id):
    temp_part_list = []
    queue_rez_list = []
    max_number = int(org_dict['Max Number'])

    if org_dict['Activity'] == 'Raid' or org_dict['Activity'] == 'Dungeon':
        beg_counter = int(org_dict['Beginner_Counter'])
        max_beg = int(org_dict['Beginners'])

        print(max_beg, beg_counter, max_beg < beg_counter)

        if org_dict['Participants']['Queue']:
            for exp in org_dict['Participants']['Queue']:
                if len(org_dict['Participants']['Participants']) < max_number:
                    org_dict['Participants']['Participants'].append(exp)
                    org_dict['Participants']['Queue'].remove(exp)
                else:
                    pass
        #             ["Sypha#5874", 496053061962170380], ["Albert#7319", 441305325719650304], ["cj_quest#7710", 534063567943499776], ["Just_FrnX#0507", 683070954603151462], ["Tala420#6469", 740857014439247902], ["Lorin Ioan Fortuna", 489214493503520778]

        _org = deepcopy(org_dict)
        participants = _org['Participants']
        author = participants['Author']

        if participants['Participants']:
            for exp in participants['Participants']:
                if not await check_if_beginner(guild, exp[1], role_id):
                    if max_beg >= beg_counter:
                        exp[0] = f"{exp[0]}🍼"
                        beg_counter += 1
                    else:
                        print(2)
                        org_dict['Participants']['Participants'].remove(exp)
                        org_dict['Participants']['Queue'].append(deepcopy(exp))
                        continue
                if exp[1] == author[1]:
                    exp[0] = f"{exp[0]}👑"
                temp_part_list.append(exp[0])

            part_list = '\n'.join(temp_part_list)
        else:
            part_list = '-'

        temp_rez_list = deepcopy(org_dict['Participants']['Queue'])

        if temp_rez_list:
            for rez in temp_rez_list:
                if not await check_if_beginner(guild, rez[1], role_id):
                    rez[0] = f"{rez[0]}🍼"
                if rez[1] == author[1]:
                    rez[0] = f"{rez[0]}👑"
                queue_rez_list.append(rez[0])

        if participants['Reserve'] or queue_rez_list:
            reserve_queue = '\n'.join(queue_rez_list)
            reserve_list = reserve_queue + '\n' + '\n'.join(
                [rez[0] if await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
                 participants['Reserve']])
        else:
            reserve_list = '-'

    else:
        if org_dict['Participants']['Queue']:
            for exp in org_dict['Participants']['Queue']:
                if len(org_dict['Participants']['Participants']) < max_number:
                    org_dict['Participants']['Participants'].append(exp)
                    org_dict['Participants']['Queue'].remove(exp)
                else:
                    pass
        _org = deepcopy(org_dict)
        participants = _org['Participants']
        author = participants['Author']

        if participants['Participants']:
            for exp in participants['Participants']:
                if exp[1] == author[1]:
                    exp[0] = f"{exp[0]}👑"
                temp_part_list.append(exp[0])
            part_list = '\n'.join(temp_part_list)
        else:
            part_list = '-'

        temp_rez_list = deepcopy(org_dict['Participants']['Queue'])

        if temp_rez_list:
            for rez in temp_rez_list:
                if rez[1] == author[1]:
                    rez[0] = f"{rez[0]}👑"
                queue_rez_list.append(rez[0])

        if participants['Reserve'] or queue_rez_list:
            reserve_queue = '\n'.join(queue_rez_list)
            reserve_list = reserve_queue + '\n' + '\n'.join(
                [rez[0] if await check_if_beginner(guild, rez[1], role_id) else f'{rez[0]}🍼' for rez in
                 participants['Reserve']])
        else:
            reserve_list = '-'

    return part_list, reserve_list, org_dict

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
    guild = await bot.fetch_guild(GUILD_ID)

    part_list, reserve_list, org_dict = await create_part_stings(org_dict, guild, role_id)
    data_manager(org_dict=org_dict, mode='a')


    author_name = org_dict['Participants']['Author'][0]

    await message.edit(content='<@&1075455824782184523> Organizare noua!', embed=OrgEmbed(org_dict, attribute_list, author_name, part_list, reserve_list),
                       view=OrgView(org_dict, attribute_list, bot))


async def init_edit(bot: commands.Bot, org_dict,):
    _, message = await get_message(bot, org_dict)
    changes = data_manager(org_dict=org_dict, mode='u')
    await edit_mesaj(_bot, message, org_dict=org_dict)
    await spam_on_edit(bot, org_dict, changes, message.jump_url)


async def edit_mesaj(bot: commands.Bot, message, org_dict, block=False):
    global _bot
    _bot = bot

    print('Initializare edit mesaj')
    attribute_list = activity_details[org_dict['Type']]
    role_id, _, _, _, _ = attribute_list
    guild = await bot.fetch_guild(GUILD_ID)

    part_list, reserve_list, org_dict = await create_part_stings(org_dict, guild, role_id)
    author_name = org_dict['Participants']['Author'][0]
    data_manager(org_dict=org_dict, mode='u')

    if org_dict['Org_info']['Active']:
        await message.edit(content='<@&1075455824782184523> Organizare noua!', embed=OrgEmbed(org_dict, attribute_list, author_name, part_list, reserve_list),
                           view=OrgView(org_dict, attribute_list, bot))
    else:
        await message.edit(content='Organizarea a inceput!', embed=OrgEmbed(org_dict, attribute_list, author_name, part_list, reserve_list),
                           view=None)


class OrgEmbed(discord.Embed):
    def __init__(self, org_dict, attribute_list, author_name, part_list, reserve_list):
        role_id, guide_id, hex_color, active_img, expired_img = attribute_list
        super().__init__(title=f"Organizare — {org_dict['Type']}",
                         description=f'',
                         color=hex_color)

        self.add_field(name='ID',
                       value=org_dict['ID'],
                       inline=True)

        self.add_field(name='‎',
                       value='‎',
                       inline=True)

        from datetime import datetime
        if int(org_dict['Datetime']) - datetime.now().timestamp() < 3600 * 5:
            date_str = f"<t:{org_dict['Datetime']}:R>"
        else:
            date_str = f"<t:{org_dict['Datetime']}:f>"

        self.add_field(name='Data si ora',
                       value=date_str,
                       inline=True)

        if org_dict['Beginners'] != '0':  # != 0 or org_dict['Beginners'] is not None
            beg_number = f"Maxim {org_dict['Beginners']} incepatori 🍼"
        else:
            beg_number = "Fara incepatori 🍼"

        if org_dict['Activity'] == 'Raid' or org_dict['Activity'] == 'Dungeon':
            self.add_field(name='Info',
                           value=f"{org_dict['Info']} \n\n**{beg_number}**",
                           inline=False)

            self.add_field(name='‎',
                           value='‎',
                           inline=False)
        else:

            self.add_field(name='Info',
                           value=org_dict['Info'],
                           inline=False)

            self.add_field(name='‎',
                           value='‎',
                           inline=False)

        '''
        Tratare participanti
        '''

        self.add_field(name=f'Participanti',
                       value=f'{part_list}',
                       inline=True)

        self.add_field(name='‎',
                       value='‎',
                       inline=True)

        self.add_field(name=f'Rezerve',
                       value=reserve_list,
                       inline=True)

        if not org_dict['Org_info']['Active']:
            image_url = expired_img
        else:
            image_url = active_img

        self.set_image(url=image_url)

        self.set_footer(text=f"Creat de {org_dict['Participants']['Author'][0]}")


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
            await spam_on_edit(interaction.client, org_dict, changes=[], deleted=True)
            await message.delete()

            data_updater(org_old=org_dict, org_new={})

    if button_label == 'join':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        if player_data in org_dict['Participants']['Participants']:
            return

        if player_data in org_dict['Participants']['Queue']:
            return

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)

        org_dict['Participants']['Queue'].append(player_data)
        await edit_mesaj(_bot, message, org_dict=org_dict)
        return

    if button_label == 'reserve':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        if player_data in org_dict['Participants']['Participants']:
            org_dict['Participants']['Participants'].remove(player_data)

        if player_data in org_dict['Participants']['Queue']:
            org_dict['Participants']['Queue'].remove(player_data)

        if player_data not in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].append(player_data)
            await author.add_roles(org_role)
            await edit_mesaj(_bot, message, org_dict=org_dict)

    if button_label == 'leave':
        author = interaction.user
        player_data = [''.join([author.nick if author.nick else author.name]), author.id]

        if player_data in org_dict['Participants']['Participants']:
            org_dict['Participants']['Participants'].remove(player_data)

        if player_data in org_dict['Participants']['Queue']:
            org_dict['Participants']['Queue'].remove(player_data)

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)

        await author.remove_roles(org_role)
        await edit_mesaj(_bot, message, org_dict=org_dict)

    # data_updater(org_old=org_old, org_new=org_dict)


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Notify Edit
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def spam_on_edit(bot: commands.Bot, org_dict, changes, jump_url='', deleted=False):

    org_id = org_dict['ID']

    for member in org_dict['Participants']['Participants']:
        if member[1] == org_dict['Participants']['Author'][1]:
            continue
        member_obj = await bot.fetch_user(member[1])
        if deleted:
            await member_obj.send(content='', embed=DeleteEmbed(org_dict))
            continue
        await member_obj.send(content='', embed=EditEmbed(org_id, changes, jump_url))

    for member in org_dict['Participants']['Queue']:
        member_obj = await bot.fetch_user(member[1])
        if deleted:
            await member_obj.send(content='', embed=DeleteEmbed(org_dict))
            continue
        await member_obj.send(content='', embed=EditEmbed(org_id, changes, jump_url))

    for member in org_dict['Participants']['Reserve']:
        member_obj = await bot.fetch_user(member[1])
        if deleted:
            await member_obj.send(content='', embed=DeleteEmbed(org_dict))
            continue
        await member_obj.send(content='', embed=EditEmbed(org_id, changes, jump_url))


class EditEmbed(discord.Embed):
    def __init__(self, id, changes, jump_url):
        super().__init__(title=f"Organizare modificata!",
                         description=f'Salut, autorul organizarii {id} la care esti inscris a facut o modificare. {jump_url}',
                         color=0x1d3fa5)

        for key in changes:
            if key == 'Datetime':
                self.add_field(name='Data si ora',
                               value=f"<t:{changes[key][1]}:f>",
                               inline=True)
                self.add_field(name='',
                               value=f"——>",
                               inline=True)
                self.add_field(name='Data si ora noua',
                               value=f"<t:{changes[key][0]}:f>",
                               inline=True)
            else:
                self.add_field(name=key,
                               value=f"{changes[key][1]}",
                               inline=True)
                self.add_field(name='',
                               value=f"——>",
                               inline=True)
                self.add_field(name=f'{key} modificat',
                               value=f"{changes[key][0]}",
                               inline=True)


class DeleteEmbed(discord.Embed):
    def __init__(self, org_dict):
        super().__init__(title=f"Organizare anulata!",
                         description=f'Salut, organizarea la care erai inscris a stearsa de catre autor!',
                         color=0xff2506)

        org_id = org_dict['ID']

        self.add_field(name=f'Activitate - ID {org_id}',
                       value=f"{org_dict['Type']}",
                       inline=False)

        self.add_field(name='Info',
                       value=f"{org_dict['Info'] if org_dict['Info'] else '-'}",
                       inline=False)

        self.add_field(name='Data si ora',
                       value=f"<t:{org_dict['Datetime']}:f>",
                       inline=False)

        self.add_field(name='Autor',
                       value=f"{org_dict['Participants']['Author'][0]}",
                       inline=False)