'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Boilerplate
—————————————————————————————————————————————————————————————————————————————————————————————————

'''

GUILD_ID = 1075455824643764314
PLAYER_UPDATES_CHANNEL = 1100486602922397776
ORG_CHANNEL = 1101037441999179827
REMINDER_CHANNEL = 1075455825788809276
WELCOME_CHANNEL = 1075455825205800974
CLAN_INVITE_CHANNEL = 1075455825377763418
AUDIT_CHANNEL = 1100487208936423556
SERVER_BOOSTER = 1101409180440592430
DONATOR_ROLE = 1075455824811532323
VIP_ROLE = 1101631680982306987
PVE_CATEGORY = 1101037807671197706
ADMIN_ROLE = 1104377935009419385
GIVEAWAY_CHANNEL = 1100475384446865468  # 1100487208936423556
TICKET_CHANNEL = 1075455825377763421


ORG_DETAILS = {
    "King's fall": {
        "ROLE_ID": 1075455824748621840,
        "HEX_COLOR": 16723712,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/KF.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/KF_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/0e515c7cf25a2f2350b788e6f5b7f8eb.png"
    },
    "Deep Stone Crypt": {
        "ROLE_ID": 1075455824765394986,
        "HEX_COLOR": 35071,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DSC.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DSC_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/9d6744eed9fa9b55f8190ce975f1872d.png"
    },
    "Garden of Salvation": {
        "ROLE_ID": 1075455824765394988,
        "HEX_COLOR": 3569664,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOS.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOS_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/e48d301e674a19f17c5cb249a2da0173.png"
    },
    "Last Wish": {
        "ROLE_ID": 1075455824765394990,
        "HEX_COLOR": 588918,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/LW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/LW_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/597d5fe665eeb011ec0d74a5d9d8137e.png"
    },
    "Vault of Glass": {
        "ROLE_ID": 1075455824765394984,
        "HEX_COLOR": 22841,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOG.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOG_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/6d2ba4628f33a6884b5d32d62eac6a32.png"
    },
    "Vow of the Disciple": {
        "ROLE_ID": 1075455824748621842,
        "HEX_COLOR": 4655362,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOW_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/b84b6ea72dd05de7123aa2ae87ba0d6a.png"
    },
    "Root Of Nightmares": {
        "ROLE_ID": 1101410490363686952,
        "HEX_COLOR": 8258969,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/RON.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/RON_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/f2b6ec58e14244e4972705897667c246.png"
    },
    "Crota\'s End": {
        "ROLE_ID": 1147460054967128104,
        "HEX_COLOR": 0x435c19,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/d89e12c918cb0c6b1087b073ad14d6c2.png"
    },
    "Salvation\'s Edge": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 0xad324d,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/4da15a79ac0497134721eb8ce11004e3.png"
    },
    "Spire of the Watcher": {
        "ROLE_ID": 1075455824731852844,
        "HEX_COLOR": 12085764,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/241785dc00e0bf32e30d0031e299cefd.png"
    },
    "Warlord\'s Ruin": {
        "ROLE_ID": 1075455824731852844,
        "HEX_COLOR": 0x113314,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/e5f919f084ce74b117a52e6c6becc98d.png"
    },
    "Duality": {
        "ROLE_ID": 1075455824731852846,
        "HEX_COLOR": 9044012,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DUAL.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DUAL_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/de980f8f4a07662455dd7fa1b3aa2169.png"
    },
    "Grasp of Averice": {
        "ROLE_ID": 1075455824731852848,
        "HEX_COLOR": 58991,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOA.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOA_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/ed7e19a3231e2eca90ae271960c1ed9c.png"
    },
    "Pit": {
        "ROLE_ID": 1075455824748621836,
        "HEX_COLOR": 6893326,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PIT.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PIT_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/b5c87175a97d1333da0ff4300fb87f57.png"
    },
    "Prophecy": {
        "ROLE_ID": 1075455824748621834,
        "HEX_COLOR": 7471305,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PROPH.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PROPH_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/8a3f7ac8bedf90190a101bbfdc981742.png"
    },
    "Shattered Throne": {
        "ROLE_ID": 1075455824748621838,
        "HEX_COLOR": 1126469,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/ST.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/ST_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/208ce44c0342f8b0691d483d9622bd96.png"
    },
    "Crucible 6v6": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 10357531,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/193fcaaf80f97c83eb10568dbe514cf1.png"
    },
    "Comp 3v3": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 5309709,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/9ea5b18e07435f1c7af10bc24d27783a.png"
    },
    "Trials 3v3": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 15120645,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/0b99a30965218b7c6638d7f83c4bde05.png"
    },
    "Gambit": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 1080080,
        "MAX_PLAYERS": 4,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT_EXP.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/ad70ec95de79beb6ce28bcdd426df56c.png"
    },
    "Nightfall": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 1188440,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/NF.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/NF_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/87271a86b4542822aad73d8f0f56d4cb.png"
    },
    "GM": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 11574116,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GM.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GM_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/87271a86b4542822aad73d8f0f56d4cb.png"
    },
    "Defiant Battlegrounds": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 10456543,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DBG.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DBG_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/dbc7edd3f5f6011f5560e91d8cdad0bc.png"
    },
    "Ghosts of the Deep": {
        "ROLE_ID": 1111895978350497882,
        "HEX_COLOR": 65597,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOTD.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOTD_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/0d982b16bff7e62c884f103303603a1a.png"
    },
    "Peste": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 41727,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PESTE.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PESTE_exp.png",
        "ICON": "https://media.discordapp.net/attachments/1060846160933306380/1157649879703769129/fish.png?ex=651960f7&is=65180f77&hm=63bc6b9b3707086d699c94830c8d8f27e8587a2be7f3706f75c02ac0a0de492e&=&width=960&height=392"
    },
    "Sesiune Raid": {
        "ROLE_ID": 77777777777,
        "HEX_COLOR": 16547587,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SES.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SES_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/6c9052b8fcaea41c2c858c39cf504687.png"
    },
    "Deep Dive": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 2361971,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DD.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DD_exp.png",
        "ICON": "https://www.bungie.net/common/destiny2_content/icons/0d982b16bff7e62c884f103303603a1a.png"
    }
}
