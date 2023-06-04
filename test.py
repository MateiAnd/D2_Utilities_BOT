import json


player_numbers = {
    "King's fall": 6,
    'Deep Stone Crypt': 6,
    'Garden of Salvation':  6,
    'Last Wish':  6,
    'Vault of Glass':  6,
    'Vow of the Disciple':  6,
    'Root Of Nightmares':  6,
    'Spire of the Watcher':  3,
    'Duality': 3,
    'Grasp of Averice': 3,
    'Pit': 3,
    'Prophecy': 3,
    'Shattered Throne': 3,
    'Crucible 6v6': 6,
    'Comp 3v3': 3,
    'Trials 3v3': 3,
    'Gambit': 4,
    'Nightfall': 3,
    'GM': 3,
    'Defiant Battlegrounds': 3,
    'Ghosts of the Deep': 3,
    'Peste': 6,
}


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
    'Defiant Battlegrounds': [1075455824782184523, None, 0x9f8ddf, r'http://buzea.pro/buzea.pro/d2ro/Assets/DBG.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/DBG_exp.png'],
    'Ghosts of the Deep': [1111895978350497882, None, 0x01003d, r'http://buzea.pro/buzea.pro/d2ro/Assets/GOTD.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/GOTD_exp.png'],
    'Peste': [1075455824782184523, None, 0x00a2ff, r'http://buzea.pro/buzea.pro/d2ro/Assets/PESTE.png', r'http://buzea.pro/buzea.pro/d2ro/Assets/PESTE_exp.png']
}


new_dict = {}
for key, value in activity_details.items():
    role_id, guide_id, hex_color, active_img, expired_img = value
    max_players = player_numbers[key]

    _temp_dict = {
        "ROLE_ID": role_id,
        # "GUIDE_ID": guide_id,
        "HEX_COLOR": hex_color,
        "MAX_PLAYERS": max_players,
        "ACTIVE_IMG": active_img,
        "EXPIRED_IMG": expired_img,
    }

    new_dict[key] = _temp_dict


with open('./org_details.json', 'w') as f:
    json.dump(new_dict, fp=f, indent=4)