import json
import discord
from discord.utils import get


global GUILD_ID, PLAYER_UPDATES_CHANNEL, SERVER_BOOSTER, DONATOR_ROLE
GUILD_ID = 1075455824643764314
PLAYER_UPDATES_CHANNEL = 1100486602922397776
SERVER_BOOSTER = 1101409180440592430
DONATOR_ROLE = 1075455824811532323


async def init(bot):
    # variabile locale
    manual_donator = []
    update_channel = await bot.fetch_channel(PLAYER_UPDATES_CHANNEL)

    # setup bot
    members = bot.get_all_members()
    server = await bot.fetch_guild(GUILD_ID)
    server_booster = server.get_role(SERVER_BOOSTER)
    donator_role = server.get_role(DONATOR_ROLE)

    # citire donatori manual
    with open('./utilities/donator_db.json') as f:
        _temp = json.load(f)
        donator_list = _temp['data']
    for don in donator_list:
        manual_donator.append(don["id"])

    # executare pt server boost
    for member in members:
        if member.id in manual_donator:
            if donator_role not in member.roles:
                print(f'{"—" * 3} Adaugat donator lui {member.nick if member.nick else member.display_name}')
                try:
                    await update_channel.send(
                        content=f'Adaugat donator lui {member.mention} din lista de donatori concursuri')
                    await member.add_roles(donator_role)
                except:
                    await update_channel.send(content=f'Pula mea nu a mers')

        elif server_booster in member.roles:
            if donator_role not in member.roles:
                print(f'{"—" * 3} Adaugat donator lui {member.nick if member.nick else member.display_name} din server boost')
                await update_channel.send(content=f'Adaugat donator lui {member.mention} din Server Boost')
                await member.add_roles(donator_role)

        # elif donator_role in member.roles:
        #     print(f'{"—" * 3} Scos donator lui {member.nick if member.nick else member.display_name}')
        #     await update_channel.send(content=f'Scos rol donator lui {member.mention}.')
        #     await member.remove_roles(donator_role)

    # executare pentru donatori manual
    for don in donator_list:
        from datetime import datetime
        donator = await server.fetch_member(don['id'])

        if donator_role in donator.roles:
            time_limit = datetime.strptime(don['time'], '%d/%m/%Y')
            if datetime.now() > time_limit:
                print(f'{"—" * 3} Scos donator lui {donator.nick if donator.nick else donator.display_name} din timp expirat')
                await update_channel.send(content=f'Scos rol donator lui {donator.mention} din expirare timp.')
                await donator.remove_roles(donator_role)
                donator_list.remove(don)

    with open('./utilities/donator_db.json', 'w') as f:
        _temp['data'] = donator_list
        json.dump(_temp, f, indent=4)
