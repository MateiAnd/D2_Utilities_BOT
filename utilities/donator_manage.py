import json
import discord
from discord.utils import get


global GUILD_ID, PLAYER_UPDATES_CHANNEL, SERVER_BOOSTER, DONATOR_ROLE
GUILD_ID = 1075455824643764314
PLAYER_UPDATES_CHANNEL = 1100486602922397776
SERVER_BOOSTER = 1101409180440592430
DONATOR_ROLE = 1075455824811532323

async def init(bot, interaction):
    await interaction.response.defer()
    donator_dict = {}
    delete_donator = {}
    members = bot.get_all_members()

    server = await bot.fetch_guild(GUILD_ID)
    server_booster = server.get_role(SERVER_BOOSTER)
    donator_role = server.get_role(DONATOR_ROLE)

    update_channel = await bot.fetch_channel(PLAYER_UPDATES_CHANNEL)

    for member in members:
        if server_booster in member.roles:
            donator_dict[member.display_name] = member.id
        elif donator_role in member.roles and not server_booster in member.roles:
            delete_donator[member.display_name] = member.id

    with open('./utilities/donator_db.json') as f:
        donator_manual = json.load(f)
        donator_list = donator_manual['data']

    for donator in donator_list:
        from datetime import datetime

        if donator['name'] in delete_donator and datetime.now() < datetime.strptime(donator['time'], '%d/%m/%Y'):
            delete_donator.pop(donator['name'])
        else:
            # aici pus await scos rol
            donator_manual['data'].remove(donator)

    with open('./utilities/donator_db.json', 'w') as f:
        json.dump(donator_manual, f, indent=4)

    print(f'Finish \n{"—" * 10}')
    await interaction.followup.send(embed=CustomEmbed_1(delete_donator))
    await interaction.followup.send(embed=CustomEmbed_2(donator_dict))
    await interaction.followup.send(embed=CustomEmbed_3(donator_manual['data']))


class CustomEmbed_1(discord.Embed):
    def __init__(self, delete_donator):
        super().__init__(title=f"Lista de donatori care trebuie stersi", color=0xc8192b)

        for not_don in delete_donator:
            self.add_field(name=f'',
                           value=f'<@{delete_donator[not_don]}>',
                           inline=False)


class CustomEmbed_2(discord.Embed):
    def __init__(self, donator_dict):
        super().__init__(title=f"Lista Boosteri", color=0xf47fff)

        for booster in donator_dict:
            self.add_field(name=f'',
                           value=f'<@{donator_dict[booster]}>',
                           inline=False)


class CustomEmbed_3(discord.Embed):
    def __init__(self, donator_manual):
        super().__init__(title=f"Lista de donatori concursuri", color=0xffc83d)

        for donator in donator_manual:
            self.add_field(name=f'',
                           value=f'<@{donator["id"]}> pana la data de __**{donator["time"]}**__',
                           inline=False)


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Adauga
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def add_donator(interaction, bot, member, time):
    await interaction.response.defer()

    server = await bot.fetch_guild(GUILD_ID)
    donator_role = server.get_role(DONATOR_ROLE)

    new_donator_dict = {'name': member.display_name,
                        'id': member.id,
                        'time': time}

    with open('./utilities/donator_db.json', 'r') as f:
        donator_manual = json.load(f)
        _temp = donator_manual['data']

        is_here = 0
        for don in _temp:
            if new_donator_dict['name'] == don['name']:
                # from datetime import datetime
                # time_new = datetime.strptime(new_donator_dict['time'], '%d/%m/%Y')
                # time_old = datetime.strptime(don['time'], '%d/%m/%Y')
                # if time_new > time_old:
                #     _temp.remove(don)
                #     _temp.append(new_donator_dict)
                is_here = 1
                _temp.remove(don)
                _temp.append(new_donator_dict)

        if not is_here:
            _temp.append(new_donator_dict)

    donator_manual['data'] = _temp

    with open('./utilities/donator_db.json', 'w') as f:
        json.dump(donator_manual, f, indent=4)

    await interaction.followup.send(content=f'Adaugat la lista de donatori {member.mention} pana pe data de **{time}**')
    await member.add_roles(donator_role)