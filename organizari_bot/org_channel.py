import BOT_setup
import copy
import json

import discord
from discord.ext import commands
from copy import deepcopy

from evidenta_populatiei.beginner_db import get_beginner_status
from organizari_bot.functions import get_org_by_msg_id, data_updater


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
    org_channel = await _bot.fetch_channel(BOT_setup.ORG_CHANNEL)
    if not org_dict['Message_id']:
        message = await org_channel.send(content='temp')
        org_dict['Message_id'] = message.id
    else:
        message = await org_channel.fetch_message(org_dict['Message_id'])

    return org_dict, message


# def time_flagger(date_string):
#     from datetime import datetime
#     date_object = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
#     time_difference = datetime.now() - date_object
#     return int(time_difference.total_seconds() / 60)


# def check_role(guild: discord.Guild, role_id, author):
#     exp_role = guild.get_role(role_id)
#     if exp_role in author.roles:
#         return True
#     return False


def check_role(role_id, author):
    if int(role_id) in [role.id for role in author.roles]:
        return True
    return False


async def check_if_beginner(guild: discord.Guild, member_id, role_id) -> bool:
    member = await guild.fetch_member(int(member_id))
    eval = check_role(role_id, member)
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

    if org_dict['Activity'] == 'Raid' or org_dict['Activity'] == 'Dungeon':  # ) and org_dict['Type'] != 'Sesiune Raid'

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

        max_beg = int(org_dict['Beginners'])
        org_dict['Beginner_Counter'] = 0

        if participants['Participants']:
            beginner_status = await get_beginner_status(participants['Participants'], role_id)
            for exp in participants['Participants']:
                if not beginner_status[exp[1]]:
                    if max_beg > org_dict['Beginner_Counter']:
                        exp[0] = f"{exp[0]}🍼"
                        org_dict['Beginner_Counter'] += 1
                    else:
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
            beginner_status = await get_beginner_status(temp_rez_list, role_id)
            for rez in temp_rez_list:
                if not beginner_status[rez[1]]:
                    rez[0] = f"{rez[0]}🍼"
                if rez[1] == author[1]:
                    rez[0] = f"{rez[0]}👑"
                queue_rez_list.append(rez[0])

        if participants['Reserve'] or queue_rez_list:
            beginner_status = await get_beginner_status(participants['Reserve'], role_id)
            reserve_queue = '\n'.join(queue_rez_list)
            reserve_list = reserve_queue + '\n' + '\n'.join(
                [rez[0] if beginner_status[rez[1]] else f'{rez[0]}🍼' for rez in
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
            reserve_list = reserve_queue + '\n' + '\n'.join([rez[0] for rez in participants['Reserve']])
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

    attribute_list = BOT_setup.ORG_DETAILS[org_dict['Type']]
    role_id = attribute_list["ROLE_ID"]

    org_dict, message = await get_message(_bot, org_dict)
    guild = await bot.fetch_guild(BOT_setup.GUILD_ID)

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
    attribute_list = BOT_setup.ORG_DETAILS[org_dict['Type']]
    role_id = attribute_list["ROLE_ID"]
    guild = await bot.fetch_guild(BOT_setup.GUILD_ID)

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
        super().__init__(title=f"Organizare — {org_dict['Type']}",
                         description=f'',
                         color=attribute_list["HEX_COLOR"])

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
            image_url = attribute_list["EXPIRED_IMG"]
        else:
            image_url = attribute_list["ACTIVE_IMG"]

        self.set_image(url=image_url)

        self.set_footer(text=f"Creat de {org_dict['Participants']['Author'][0]}")


class OrgView(discord.ui.View):
    def __init__(self, org_dict, attribute_list, bot):
        super().__init__(timeout=None)

        self.role_id = attribute_list["ROLE_ID"]

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
                                   guild=interaction.guild, message=message)

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

    org_role = guild.get_role(org_dict['Org_utils']['Part'])

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

        role_id = BOT_setup.ORG_DETAILS[org_dict['Type']]["ROLE_ID"]
        beginner_status = await get_beginner_status([player_data], role_id)

        if player_data not in org_dict['Participants']['Participants'] and player_data not in org_dict['Participants']['Queue'] and player_data not in org_dict['Participants']['Reserve']:
            return

        if not beginner_status[author.id]:
            org_dict['Beginner_Counter'] -= 1

        if player_data in org_dict['Participants']['Participants']:
            org_dict['Participants']['Participants'].remove(player_data)

        if player_data in org_dict['Participants']['Queue']:
            org_dict['Participants']['Queue'].remove(player_data)

        if player_data in org_dict['Participants']['Reserve']:
            org_dict['Participants']['Reserve'].remove(player_data)

        await author.remove_roles(org_role)
        await edit_mesaj(_bot, message, org_dict=org_dict)
        data_manager(org_dict=org_dict, mode='u')

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
        if member[1] == org_dict['Participants']['Author'][1]:
            continue
        member_obj = await bot.fetch_user(member[1])
        if deleted:
            await member_obj.send(content='', embed=DeleteEmbed(org_dict))
            continue
        await member_obj.send(content='', embed=EditEmbed(org_id, changes, jump_url))

    for member in org_dict['Participants']['Reserve']:
        if member[1] == org_dict['Participants']['Author'][1]:
            continue
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