import BOT_setup
import discord
from discord.ext import commands
import json

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Trimite msaje
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


def write_data(_dict):
    with open('./giveaway/giveaway_setup.json', 'w') as f:
        json.dump(_dict, f)


async def create_accept_entries(bot: commands.Bot):
    with open('./giveaway/giveaway_setup.json', 'w') as f:
        giveaway_dict = json.load(f)

        if not giveaway_dict:
            return

    rigged_winners = giveaway_dict['Rig']
    proposed_winners = giveaway_dict['ProposedWinners']

    channel = await bot.fetch_channel(BOT_setup.AUDIT_CHANNEL)

    for member in proposed_winners:
        if member in rigged_winners:
            await channel.send(content='', embed=AcceptEmbed(member), view=None)
        else:
            await channel.send(content='', embed=DetermineEmbed(member), view=DetermineView(giveaway_dict, member))


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Embed
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


class DetermineEmbed(discord.Embed):
    def __init__(self, member):
        super().__init__(title="Verifica eligibilitate",
                         description=f'Se accepta {member} ca castigator al giveaway-ului?',
                         color=0xe7eb07)


class DetermineView(discord.ui.View):
    def __init__(self, giveaway_dict, member, ):
        super().__init__(timeout=None)

        button_labels = ['✅', '❌']

        for elem in button_labels:
            button = DetermineMessageButtons(giveaway_dict, member, elem)
            self.add_item(button)


class DetermineMessageButtons(discord.ui.Button):
    def __init__(self, giveaway_dict, member, label):
        if label == '✅':
            super().__init__(label=label, style=discord.ButtonStyle.success)

            async def callback(interaction: discord.Interaction):
                giveaway_dict['AcceptedWinners'].append(member)
                giveaway_dict['ProposedWinners'].remove(member)

                write_data(giveaway_dict)
                await interaction.message.edit(content='', embed=AcceptEmbed(member), view=None)
        else:
            super().__init__(label=label, style=discord.ButtonStyle.danger)

            async def callback(interaction: discord.Interaction):
                giveaway_dict['DeclinedWinners'].append(member)
                giveaway_dict['ProposedWinners'].remove(member)

                write_data(giveaway_dict)
                await interaction.message.edit(content='', embed=DeclineEmbed(member), view=None)

        self.callback = callback


class AcceptEmbed(discord.Embed):
    def __init__(self, member):
        super().__init__(title="Verificat!",
                         description=f'Membrul {member} a fost verificat!',
                         color=0x22eb07)


class DeclineEmbed(discord.Embed):
    def __init__(self, member):
        super().__init__(title='Refuzat!',
                         description=f'Membrul {member} a fost refuzat!',
                         colour=0xff0000)
