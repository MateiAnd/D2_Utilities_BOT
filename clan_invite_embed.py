import discord
import contact_destiny_api
from discord.ext import tasks


class ClanEmbed(discord.Embed):
    def __init__(self, clan_numbers):
        super().__init__(title="CLAN LINKS", color=0xc75450)

        self.url_dict = {
            'A': 'https://www.bungie.net/en/ClanV2?groupid=5071579',  # 'https://cdn.discordapp.com/attachments/752509452279742545/1092133330285244497/360_F_315942126_eVHcsAL0e2z9OW3yNLBJ8JpeQorDFlQj.png',
            'B': 'https://www.bungie.net/en/ClanV2?groupid=4397838',
            'X': 'https://www.bungie.net/en/ClanV2/Index?groupId=4613286'
        }

        self.clan_admin = {
            'A': [489214493503520778, 496053061962170380],
            'B': [527863507270631445],
            'X': [740857014439247902]
        }

        self.set_author(name='Destiny 2 Romania',
                        icon_url='https://cdn.discordapp.com/attachments/1101368918318260274/1101498772560806001/logo_mic.png')
        self.set_thumbnail(url='https://www.pngitem.com/pimgs/m/63-636562_join-us-won-t-you-hd-png-download.png')


        self.add_field(name='',
                       value=f'Ultimele 5 locuri din clan sunt rezervate pentru membri ai comunitatii care doresc sa completeze triumfe! \n \n{"—" * 30}',
                       inline=False)


        for clan in clan_numbers:
            ping_str = ' '.join([f'<@{user}>' for user in self.clan_admin[clan]])
            if clan_numbers[clan] > 5:
                locuri_clan = f"{clan_numbers[clan]} locuri libere"
            elif clan_numbers[clan] <= 5:
                locuri_clan = f"CLAN PLIN \n{clan_numbers[clan]} locuri rezervate"
            else:
                locuri_clan = "CLAN PLIN"

            # if clan == 'A':
            #     locuri_clan = 'CLAN INCHIS'

            self.add_field(name='',
                           value=f'Clan {"<:steam:1101491300777328641>" if clan != "X" else "<:controller:1104805174368813179>"} [Destiny 2 Romania #{clan}]({self.url_dict[clan]}) **{locuri_clan}** \n Contact: {ping_str} \n {"—" * 25} \n',
                           inline=False)

        self.set_footer(text='© Destiny 2 Romania',
                        icon_url='https://cdn.discordapp.com/attachments/1101368918318260274/1101498772560806001/logo_mic.png')


async def init(interaction, bot):
    global msg_id

    await interaction.response.send_message(content='Asteapta', ephemeral=True)
    channel = interaction.channel

    clan_numbers = get_clan_stats()

    # await interaction.followup.send(content='', embed=ClanEmbed(clan_numbers))
    # message_ = await interaction.original_response()

    massage = await channel.send(content='', embed=ClanEmbed(clan_numbers))
    with open('embed_msg.txt', 'w') as f:
        f.write(str(massage.id))

    # do_refresh_embed.start(massage)

    print(f'Finish \n{"—" * 10}')


def get_clan_stats():
    clan_numbers = {}
    letters = ['A', 'B', 'X']

    for letter in letters:
        clan_dict = contact_destiny_api.get_destiny_clan_memebrs_by_letter(letter)
        clan_numbers[letter] = (100 - len(clan_dict))
    return clan_numbers


# @tasks.loop(minutes=60)
# async def do_refresh_embed(message):
#     print(f'{"—" * 5} Refresh embed clan link {"—" * 5}')
#     clan_numbers = get_clan_stats()
#     await message.edit(content='', embed=ClanEmbed(clan_numbers))





