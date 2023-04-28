# D2_Utilites_BOT
***

A general description of the commands and the use cases of all the functions this Discord bot is tasked with.

***
## 1. Management commands

These are administrator-only commands and should not be used without knowledge of theis functions and effects.

---
``/generate_clan_invite_embed`` 

This command will generate a 'CLAN LINKS' embedded message in channel 'join-clan-steps' (<#938290015195238400>). 
Once created, the message will self-update once an hour, checking the clan data requested from Bungie API, updating the 
available spaces left in the clan.

**Warning:** This command will not delete a previously sent embedded message. 
The previous message will stop updating if a new message is generated, as it will be replaced as the target in the 
update function. Manual deletion is necessary if the message existed before sending this command. 

---
``/curatenie_generala @role_call``

This command will generate an embedded message as a response to the command. This will check all the Discord users with 
the role **@role_call** and the data requested from the Bungie API.

Two data lines will be generated in the embedded message, if it is necessary:

- **————— Overdue —————** 

If a clan member is inactive for more than 60 days in-game, he will be displayed under this category, with the number 
of days past 60 days. 
Example: '🕒 dani#0343 inactiv 66 zile'

- **————— Not Found —————**

If a clan member is not found in the Discord member list, he will be displayed in this category and be marked for removal.

---

## 2. Management functions

The bot will send updates of player activity in the channel 'player-updates' (<#1086041802831843359>). The update
regarding this section is an on member leave event. This event will send a message containing their nickname 
(Destiny 2 username) or their Discord account name if the nickname is not available. If the member was a part of a clan,
this will be signaled by adding the clan role mention in the message, marking the clan member for removal by the clan admins.

Example: 

'Membrul Jovil#5241 a iesit si facea parte din @KH Clan C'

'Membrul DarkuS230#4726 a iesit'

'Membrul Raull a iesit'

---

## 3. Greeting message

The bot will aid with greeting new members to the server. It does this in two steps:

1. **Player greeting message** sent in the channel 'welcome-corner' (<#954083245522313266>). This is a static message 
formated with the member's name. This message contains general instructions about the registration steps and general info.
2. **Support thread** is a message thread started from the previously sent message. More information in the 
'Support Bot' section

---

## 4. Managing donators commands

Due to increased difficulty of managing donators, two command were created to aid with the process:

- ``/donator_check``

Will return a max of 3 embedded messages. A list of members that do not meet the donator criteria. A list of Server 
Boosters. A list of donators that were manually added by the admins, next to a datetime of the expiration date of the role.

- ``/donator_add @member year:int month:int day:int``

This command will add the member to the donator list. An expiration date of the donator role is mandatory. Manually 
adding a donator can be verified by the automatic logging message in channel 'player-updates' (<#1086041802831843359>)

---

## 5. Managing donators functions

On a timer of 30 minutes, the bot is tasked to check all the members for role updates. If a members boosts the server, 
Discord will automatically assign the 'Server Booster' role to them. If a player acquires or looses the 'Server Booster'
role, the bot will automatically manage the 'Donator' role for the admins.

The expiration date of the manually added donators is needed for automatic donator list removal. The bot checks if a 
donator is past their expiration date, and will remove the role if necessary.

---

## 6. Donator commands

To improve donator experience on the server, for the time being, one donator-specific command was added.

``/trasnfer #voice_channel``

This command allows a donator to transfer themselves from a voice channel to another voice channel, regardless if the 
target channel's player limit was archived. This allows them to be the 7th member in a 6 member Raid channel, for example.


---

## 7. General member commands

An event scheduler was added for the players. This is different from the existing event scheduler, as the use case is
fundamentally different. This scheduler is dedicated to beginner-friendly activities. A simplified interaction interface
aid the process of choosing the correct players for the activity event.

---

- ``/sherpa create``

This command will start the event creation process. The steps are as follows:

1. Activity type, choices: Raid ; Dungeon
2. Location , choices depend on the type chosen, see below
3. Date and time of the event, defaults to 15 minutes past current time\
4. Numbers of beginners allowed
5. Info screen, the user can add extra info and submit the event for creation

The activity type dictates the location choices that the player has access to. The tree style structure is as follows:

- Raid
    - "King's fall"
    - 'Deep Stone Crypt'
    - 'Garden of Salvation'
    - 'Last Wish'
    - 'Vault of Glass'
    - 'Vow of the Disciple'
    - 'Root Of Nightmares'
- Dungeon
    - 'Spire of the Watcher'
    - 'Duality'
    - 'Grasp of Averice'
    - 'Pit'
    - 'Prophecy'

If the creation process is completed and the event is submitted, an embedded message wil be sent to channel 'organizari'
(<#745904725983101017>). The message is attached to a button view, and the buttons have the functions described below:

- **Join** — will add players to their respective column (Beginner / Expert) based on the player's statistics requested 
from the Bungie API
- **Leave** — if a member joined the event and wants to leave, this button will remove them from the event
- **Reserve** — if a player does not want to join, but may be available at that time if they need another player or if 
the event is completely booked, the player can press this button to be added to an infinite Reserve list
- **Delete** — the organiser of the event can cancel it at any time, by pressing this button

---

``/sherpa edit id:int``

This command is called with the event ID, found in the event message in channel 'organizari' (<#745904725983101017>).
Successfully calling the command will start the editing process, that is the same as the creation process, see steps above
for details.

---

## 8. Support Bot

Due to ever-increasing game difficulty and server registration steps (thank you scam bots), a support chatbot was created
to aid new members and the existing server player-base.

This is a gpt-3.5-turbo derived chatbot, tasked and trained to aid new and existing players with questions regarding 
the server and the game. Continuous updates are made to the model for better performance.

The support bot can be accessed in two ways:
1. In the support thread on the welcome message of a new member
2. Calling the `/support` command (in the future) in any text channel