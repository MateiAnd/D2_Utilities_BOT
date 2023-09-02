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
ADMIN_ROLE = 1075455824811532324


ORG_DETAILS = {
    "King's fall": {
        "ROLE_ID": 1075455824748621840,
        "HEX_COLOR": 16723712,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/KF.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/KF_exp.png"
    },
    "Deep Stone Crypt": {
        "ROLE_ID": 1075455824765394986,
        "HEX_COLOR": 35071,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DSC.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DSC_exp.png"
    },
    "Garden of Salvation": {
        "ROLE_ID": 1075455824765394988,
        "HEX_COLOR": 3569664,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOS.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOS_exp.png"
    },
    "Last Wish": {
        "ROLE_ID": 1075455824765394990,
        "HEX_COLOR": 588918,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/LW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/LW_exp.png"
    },
    "Vault of Glass": {
        "ROLE_ID": 1075455824765394984,
        "HEX_COLOR": 22841,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOG.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOG_exp.png"
    },
    "Vow of the Disciple": {
        "ROLE_ID": 1075455824748621842,
        "HEX_COLOR": 4655362,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/VOW_exp.png"
    },
    "Root Of Nightmares": {
        "ROLE_ID": 1101410490363686952,
        "HEX_COLOR": 8258969,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/RON.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/RON_exp.png"
    },
    "Crota\'s End": {
        "ROLE_ID": 1147460054967128104,
        "HEX_COLOR": 0x435c19,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/CRE_exp.png"
    },
    "Spire of the Watcher": {
        "ROLE_ID": 1075455824731852844,
        "HEX_COLOR": 12085764,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SOTW_exp.png"
    },
    "Duality": {
        "ROLE_ID": 1075455824731852846,
        "HEX_COLOR": 9044012,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DUAL.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DUAL_exp.png"
    },
    "Grasp of Averice": {
        "ROLE_ID": 1075455824731852848,
        "HEX_COLOR": 58991,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOA.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOA_exp.png"
    },
    "Pit": {
        "ROLE_ID": 1075455824748621836,
        "HEX_COLOR": 6893326,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PIT.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PIT_exp.png"
    },
    "Prophecy": {
        "ROLE_ID": 1075455824748621834,
        "HEX_COLOR": 7471305,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PROPH.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PROPH_exp.png"
    },
    "Shattered Throne": {
        "ROLE_ID": 1075455824748621838,
        "HEX_COLOR": 1126469,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/ST.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/ST_exp.png"
    },
    "Crucible 6v6": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 10357531,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_6v6_exp.png"
    },
    "Comp 3v3": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 5309709,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_comp_exp.png"
    },
    "Trials 3v3": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 15120645,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PVP_trials_exp.png"
    },
    "Gambit": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 1080080,
        "MAX_PLAYERS": 4,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GAMBIT_EXP.png"
    },
    "Nightfall": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 1188440,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/NF.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/NF_exp.png"
    },
    "GM": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 11574116,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GM.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GM_exp.png"
    },
    "Defiant Battlegrounds": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 10456543,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DBG.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DBG_exp.png"
    },
    "Ghosts of the Deep": {
        "ROLE_ID": 1111895978350497882,
        "HEX_COLOR": 65597,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOTD.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/GOTD_exp.png"
    },
    "Peste": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 41727,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PESTE.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/PESTE_exp.png"
    },
    "Sesiune Raid": {
        "ROLE_ID": 77777777777,
        "HEX_COLOR": 16547587,
        "MAX_PLAYERS": 6,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SES.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/SES_exp.png"
    },
    "Deep Dive": {
        "ROLE_ID": 1075455824782184523,
        "HEX_COLOR": 2361971,
        "MAX_PLAYERS": 3,
        "ACTIVE_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DD.png",
        "EXPIRED_IMG": "https://buzea.pro/buzea.pro/d2ro/Assets/DD_exp.png"
    }
}
