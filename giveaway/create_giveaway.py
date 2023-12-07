import BOT_setup
import copy
import json
import aiofiles

import discord
from discord.ext import commands
from copy import deepcopy

from giveaway.accept_winners import create_accept_entries, write_data

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Functii main
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def create_giveaway(interaction, bot):
    await interaction.response.defer()

    global _bot
    _bot = bot

    # Verify if a giveaway is active
    with open('./giveaway/giveaway_setup.json', 'r') as f:
        give = json.load(f)
        if give:
            await interaction.followup.send(
                content='Un giveaway este deja activ. Foloseste comanda `edit` pentru a modifica givewaway-ul activ')
            return

    with open('./giveaway/giveaway_members.txt', 'w') as f:
        f.write('')

    _, _, datetime_obj = create_one_week_later_time()

    give_dict = {
        'Datetime': datetime_obj.timestamp(),
        'Prize': 'Cheie Xbox/PC game pass',
        'Number': 1,
        'Rig': [],
        'ProposedWinners': [],
        'DeclinedWinners': [],
        'AcceptedWinners': [],
        'MessageID': 0,
        'Editing': False
    }

    global message
    message = await interaction.followup.send(content='', embed=FirstEmbed(give_dict), view=FirstView(give_dict))


async def edit_giveaway(interaction, bot):
    await interaction.response.defer()

    global _bot
    _bot = bot

    # Verify if a giveaway is active
    with open('./giveaway/giveaway_setup.json', 'r') as f:
        give_dict = json.load(f)
        if not give_dict:
            await interaction.followup.send(
                content='Nu este un giveaway activ. Foloseste comanda `create` pentru a crea unul')
            return

    give_dict['Editing'] = True

    global message
    message = await interaction.followup.send(content='', embed=FirstEmbed(give_dict), view=FirstView(give_dict))


async def rig_giveaway(interaction, bot, member_id):
    global _bot
    _bot = bot

    with open('./giveaway/giveaway_setup.json', 'r') as f:
        give_dict = json.load(f)
        if not give_dict:
            await interaction.followup.send(
                content='Nu este un giveaway activ. Foloseste comanda `create` pentru a crea unul')
            return

    if len(give_dict['Rig']) < give_dict['Number']:
        give_dict['Rig'].append(member_id)

        with open('./giveaway/giveaway_setup.json', 'w') as f:
            json.dump(give_dict, f)

        await interaction.response.send_message(content=f'Adaugat membru <@{member_id}> ca castigator', ephemeral=True)
    else:
        await interaction.response.send_message(
            content=f'Numarul de castigatori rigged este mai mare decat numarul de premii, scoate o persoana cu comanda `unrig` ',
            ephemeral=True)


async def delete_giveaway(interaction, bot):
    global _bot
    _bot = bot

    with open('./giveaway/giveaway_setup.json', 'r') as f:
        giveaway_dict = json.load(f)
        if not giveaway_dict:
            await interaction.followup.send(
                content='Nu este un giveaway activ.')
            return

    giveaway_channel = await _bot.fetch_channel(BOT_setup.GIVEAWAY_CHANNEL)
    giveaway_message = await giveaway_channel.fetch_message(giveaway_dict['MessageID'])
    await giveaway_message.delete()

    with open('./giveaway/giveaway_setup.json', 'w') as f:
        json.dump({}, f)


async def unrig_giveaway(interaction, bot, member_id):
    global _bot
    _bot = bot

    with open('./giveaway/giveaway_setup.json', 'r') as f:
        give_dict = json.load(f)
        if not give_dict:
            await interaction.followup.send(
                content='Nu este un giveaway activ. Foloseste comanda `create` pentru a crea unul')
            return

    if member_id in give_dict['Rig']:
        give_dict['Rig'].remove(member_id)
        with open('./giveaway/giveaway_setup.json', 'w') as f:
            json.dump(give_dict, f)

    await interaction.response.send_message(content=f'Scos membru <@{member_id}> ca castigator', ephemeral=True)


async def giveaway_refresher(bot, giveaway_channel_id):
    with open('./giveaway/giveaway_setup.json', 'r') as f:
        give = json.load(f)

    if not give:
        return

    giveaway_channel = await bot.fetch_channel(giveaway_channel_id)
    giveaway_message = await giveaway_channel.fetch_message(give['MessageID'])

    allowed_mentions = discord.AllowedMentions(everyone=True)
    await giveaway_message.edit(content='@everyone', allowed_mentions=allowed_mentions,
                                embed=FinalEmbed(give), view=FinalView())


async def extract_giveaway_winner(bot):
    global _bot
    _bot = bot

    with open('./giveaway/giveaway_setup.json', 'r') as f:
        giveaway_dict = json.load(f)

    prize_number = giveaway_dict['Number']
    rigged_winners = giveaway_dict['Rig']

    async with aiofiles.open('./giveaway/giveaway_members.txt', 'r') as f:
        members = await f.read()

    members_list = members.split('\n')
    members_list = [int(mem) for mem in members_list if mem]
    members_list = list(set(members_list))

    # Trateaza rigged winners
    for rig in rigged_winners:
        if rig in members_list:
            members_list.remove(rig)
        else:
            rigged_winners.remove(rig)

    final_prize_number = prize_number - len(rigged_winners)

    if final_prize_number > 0:
        # Extrage legit winnners
        if len(members_list) <= final_prize_number:
            legit_winners = members_list
        else:
            import random
            legit_winners = random.sample(members_list, final_prize_number)

        # Trimite mesaj
        winners = rigged_winners + legit_winners
        giveaway_dict['ProposedWinners'] = winners
    else:
        giveaway_dict['ProposedWinners'] = rigged_winners

    write_data(giveaway_dict)
    await create_accept_entries(bot)


async def redraw_declined_winners(bot):
    global _bot
    _bot = bot

    with open('./giveaway/giveaway_setup.json', 'r') as f:
        giveaway_dict = json.load(f)

    declined_winners = giveaway_dict['DeclinedWinners']
    final_prize_number = len(declined_winners)

    async with aiofiles.open('./giveaway/giveaway_members.txt', 'r') as f:
        members = await f.read()

    members_list = members.split('\n')
    members_list = [int(mem) for mem in members_list if mem]
    members_list = list(set(members_list))

    new_winners = []

    import random
    while len(new_winners) < final_prize_number:
        new_winners.append(random.sample(members_list, final_prize_number - len(new_winners)))
        new_winners = list(set(new_winners))

        for winner in new_winners:
            if winner in declined_winners:
                new_winners.remove(winner)
            else:
                final_prize_number -= 1
                declined_winners.remove(winner)

    giveaway_dict['ProposedWinners'] = new_winners

    write_data(giveaway_dict)
    await create_accept_entries(bot)


async def send_winner_messages(giveaway_dict):
    winner_format = [f'<@{win}>' for win in giveaway_dict['AcceptedWinners']]
    winner_str = ' ; '.join(winner_format)

    giveaway_channel = await _bot.fetch_channel(BOT_setup.GIVEAWAY_CHANNEL)
    giveaway_message = await giveaway_channel.fetch_message(giveaway_dict['MessageID'])
    await giveaway_message.edit(content='', embed=ExpiredEmbed(winner_str, giveaway_dict['Prize']), view=None)


def create_one_week_later_time():
    import datetime
    import pytz

    # Get the current server's time (naive datetime)
    current_server_time_naive = datetime.datetime.now()

    # Localize the current server's time to the server's timezone
    server_timezone = pytz.utc.localize(current_server_time_naive)

    # Convert the server's current time to Bucharest timezone
    bucharest_timezone = pytz.timezone("Europe/Bucharest")
    bucharest_time = server_timezone.astimezone(bucharest_timezone)

    # Add 15 min
    after_1_week = bucharest_time + datetime.timedelta(weeks=1)  # calculate 15 minutes after current datetime
    formatted_datetime = after_1_week.strftime('%d/%m/%Y %H:%M')
    data_str, ora_str = formatted_datetime.split(' ')

    return data_str, ora_str, after_1_week


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Primul Embed - Datetime
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


class FirstEmbed(discord.Embed):
    def __init__(self, give_dict):
        if give_dict['Editing'] == True:
            title = f"Editeaza un giveaway."
        else:
            title = f"Creaza un nou giveaway."

        super().__init__(title=title,
                         description=f"""Timp selectat actual: <t:{int(round(float(give_dict['Datetime']), 0))}:f>
                         Premiul actual: {give_dict['Number']}x {give_dict['Prize']}
                         """,
                         color=0xffa600)


class FirstView(discord.ui.View):
    def __init__(self, giveaway_dict):
        super().__init__(timeout=None)

        _lista_elemente = ['Timp', 'Premiu', "Preview", 'Cancel']

        for elem in _lista_elemente:
            button = FirstMsgButtons(giveaway_dict, elem)
            self.add_item(button)


class FirstMsgButtons(discord.ui.Button):
    def __init__(self, giveaway_dict, button_label):
        self.button_label = button_label

        if self.button_label == 'Cancel':
            super().__init__(label=self.button_label, style=discord.ButtonStyle.danger)

            async def click(interaction: discord.Interaction):
                await interaction.response.defer()

                if giveaway_dict['Editing']:
                    string = f"Editare giveaway a fost anulata."
                else:
                    string = 'Creare giveaway anulata.'

                await message.edit(content=string, embed=None, view=None)

        elif self.button_label == 'Timp':
            super().__init__(label=self.button_label, style=discord.ButtonStyle.blurple)

            async def click(interaction: discord.Interaction):
                modal = DatetimeModal(giveaway_dict=giveaway_dict)
                await interaction.response.send_modal(modal)

        elif self.button_label == 'Premiu':
            super().__init__(label=self.button_label, style=discord.ButtonStyle.blurple)

            async def click(interaction: discord.Interaction):
                modal = PrizeModal(giveaway_dict=giveaway_dict)
                await interaction.response.send_modal(modal)

        else:
            super().__init__(label=self.button_label, style=discord.ButtonStyle.green)

            async def click(interaction: discord.Interaction):
                await interaction.response.defer()
                await message.edit(content='', embed=FinalEmbed(giveaway_dict),
                                   view=PreviewView(giveaway_dict=giveaway_dict))

        self.callback = click


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Modale - Datetime si Premiu
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


class DatetimeModal(discord.ui.Modal):
    def __init__(self, giveaway_dict):
        self.giveaway_dict = giveaway_dict

        if giveaway_dict['Editing'] == True:
            from datetime import datetime
            datetime_obj = datetime.fromtimestamp(giveaway_dict['Datetime'])
            data_str, ora_str = datetime_obj.strftime('%d/%m/%Y %H:%M').split(' ')
        else:
            data_str, ora_str, _ = create_one_week_later_time()

        ora = discord.ui.TextInput(
            label='Adauga ora [RO] - format 24h hh:mm',
            placeholder='Ex: 20:00',
            default=ora_str,
            required=True,
        )

        data = discord.ui.TextInput(
            label='Adauga data [RO] - format DD/MM/YYYY',
            placeholder='Ex: 15/12/2020',
            default=data_str,
            required=True,
        )
        super().__init__(title='Adauga data si ora')

        self.add_item(ora)
        self.add_item(data)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        import datetime, pytz

        ora, data = self.children
        timp_str = f'{data.value} {ora.value}'
        datetime_obj = datetime.datetime.strptime(timp_str, '%d/%m/%Y %H:%M')
        source_tz = pytz.timezone("Europe/Bucharest")
        dt = source_tz.localize(datetime_obj)

        # Convert the datetime object to epoch time in the server's local timezone
        epoch_time = dt.timestamp()
        self.giveaway_dict['Datetime'] = epoch_time

        if datetime.datetime.now().timestamp() < epoch_time:
            await message.edit(content='', embed=FirstEmbed(self.giveaway_dict), view=FirstView(self.giveaway_dict))
        else:
            await interaction.response.send_modal(DatetimeModal(self.giveaway_dict))


class PrizeModal(discord.ui.Modal):
    def __init__(self, giveaway_dict):
        self.giveaway_dict = giveaway_dict

        premiu = discord.ui.TextInput(
            label='Schimba premiul pentru giveaway - format str',
            placeholder='Ex: Cheie Xbox/PC Game Pass',
            default=self.giveaway_dict['Prize'],
            required=True,
        )
        bucati = discord.ui.TextInput(
            label='Schimba numarul de bucati - format int',
            placeholder='Ex: 1',
            default=self.giveaway_dict['Number'],
            required=True,
        )

        super().__init__(title='Modifica Premiul')

        self.add_item(premiu)
        self.add_item(bucati)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        premiu, bucati = self.children

        self.giveaway_dict['Prize'] = premiu.value
        try:
            self.giveaway_dict['Number'] = int(bucati.value)
        except:
            await interaction.response.send_modal(PrizeModal(self.giveaway_dict))

        await message.edit(content='', embed=FirstEmbed(self.giveaway_dict), view=FirstView(self.giveaway_dict))
        return


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Final - Preview
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


class FinalEmbed(discord.Embed):
    def __init__(self, give_dict):
        if give_dict['Number'] > 1:
            _temp_prize_string = f"Premile acordate sunt **{give_dict['Number']}x {give_dict['Prize']}**."
        else:
            _temp_prize_string = f"Premiul acordat este **{give_dict['Number']}x {give_dict['Prize']}**"

        super().__init__(title=f"🎁 GHRO — giveaway! 🎁",
                         description=f"""                         
                         🌟 Suntem încântați să vă anunțăm cel mai recent Giveaway! Este foarte ușor să participi și ai șansa de a câștiga premii!
                         
                         🏆 **Detalii despre Premiu:**
                         
                         {_temp_prize_string}
                         
                         📅 **Durata Concursului:**
                         
                         Concursul începe acum și se încheie pe <t:{int(round(float(give_dict['Datetime']), 0))}:f>. Nu ratați!
                         
                         🥇 **Anunțarea Câștigătorului:**
                         
                         Câștigătorul norocos va fi selectat aleatoriu și anunțat pe <t:{int(round(float(give_dict['Datetime']), 0))}:f>.
                         
                         🎉 **Cum să intri în concurs:**
                         
                         1. Apasă pur și simplu butonul 'Join'\.
                         2. Atât! Ești acum în cursa pentru a câștiga!
                         
                         👥 Toți membrii comunității noastre sunt bineveniți să participe! Alăturați-vă pentru șansa de a câștiga și de a vă distra cu comunitatea noastră. Mult noroc tuturor participanților!
                         
                         """,
                         color=0x4287f5)


class FinalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        global member_cache
        member_cache = set()

        button = FinalMsgButtons()
        self.add_item(button)


class FinalMsgButtons(discord.ui.Button):
    def __init__(self):

        super().__init__(label='Join', style=discord.ButtonStyle.success)

        async def click(interaction: discord.Interaction):
            await interaction.response.defer()

            # Verifica daca e deja inscris

            if interaction.user.id in member_cache:
                await interaction.followup.send(content='Deja ai fost inscris in giveaway. Good luck!!', ephemeral=True)
                return
            else:
                member_cache.add(interaction.user.id)

            async with aiofiles.open('./giveaway/giveaway_members.txt', 'r') as f:
                members = await f.read()

            if str(interaction.user.id) in members:
                await interaction.followup.send(content='Deja ai fost inscris in giveaway. Good luck!', ephemeral=True)
                return
            else:
                async with aiofiles.open('./giveaway/giveaway_members.txt', 'a') as f:
                    await f.write(f"{interaction.user.id}\n")
                await interaction.followup.send(content='Ai fost inscris in giveaway. Good luck!', ephemeral=True)

        self.callback = click


class PreviewView(discord.ui.View):
    def __init__(self, giveaway_dict):
        super().__init__(timeout=None)

        _lista_elemente = ['Send', 'Cancel']

        for elem in _lista_elemente:
            button = PreviewMsgButtons(giveaway_dict, elem)
            self.add_item(button)


class PreviewMsgButtons(discord.ui.Button):
    def __init__(self, giveaway_dict, button_label):
        self.button_label = button_label

        if self.button_label == 'Cancel':
            super().__init__(label=self.button_label, style=discord.ButtonStyle.danger)

            async def click(interaction: discord.Interaction):
                await interaction.response.defer()

                if giveaway_dict['Editing'] == True:
                    string = f"Editare giveaway a fost anulata."
                else:
                    string = 'Creare giveaway anulata.'

                await message.edit(content=string, embed=None, view=None)

        else:
            super().__init__(label=self.button_label, style=discord.ButtonStyle.success)

            async def click(interaction: discord.Interaction):
                await interaction.response.defer()

                # Trimite mesaj
                giveaway_channel = await _bot.fetch_channel(BOT_setup.GIVEAWAY_CHANNEL)
                allowed_mentions = discord.AllowedMentions(everyone=True)

                if giveaway_dict['Editing']:
                    giveaway_message = await giveaway_channel.fetch_message(giveaway_dict['MessageID'])
                    await giveaway_message.edit(content='@everyone', allowed_mentions=allowed_mentions,
                                                embed=FinalEmbed(giveaway_dict), view=FinalView())
                    giveaway_dict['Editing'] = False

                    string = 'Giveaway editat cu succes!'
                else:
                    giveaway_message = await giveaway_channel.send(content='@everyone',
                                                                   allowed_mentions=allowed_mentions,
                                                                   embed=FinalEmbed(giveaway_dict), view=FinalView())
                    giveaway_dict['MessageID'] = giveaway_message.id

                    string = 'Giveaway creat cu succes!'

                with open('./giveaway/giveaway_setup.json', 'w') as f:
                    json.dump(giveaway_dict, f)

                await message.edit(content=string, embed=None, view=None)

        self.callback = click


class ExpiredEmbed(discord.Embed):
    def __init__(self, winners, prize):
        super().__init__(title=f"GHRO — giveaway finalizat!",
                         description=f"""Ne bucurăm să anunțăm câștigătorii giveaway-ului. 
                         Mulțumim tuturor celor care au participat!
                         
                         **🎉 Felicitari {winners}! 🎉**
                         
                         Premiul castigat **{prize}**
                         
                         Pentru a intra în posesia premiului, va trebui să creați un ticket pe <#{BOT_setup.TICKET_CHANNEL}> și un membru <@&{BOT_setup.ADMIN_ROLE}> vă va asista în cel mai scurt timp posibil.
                         
                         
                         Urmăriți-ne pentru mai multe concursuri și premii pe viitor! GLHF!
                         """,
                         color=0x8a4cfc)
