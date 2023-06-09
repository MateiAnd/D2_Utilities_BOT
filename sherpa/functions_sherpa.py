import json


def get_org_by_msg_id(msg_id: int):
    with open('./sherpa/org_sherpa.json', 'r') as f:
        _temp = json.load(f)
    org_data = _temp['org']
    for org in org_data:
        if org["Message_id"] == msg_id:
            return org
    else:
        return {}


def make_reminder_string(org_dict, letter: str, time: str):
    participants = org_dict['Participants']

    template_string = '''{letter} mai ramas __**{timp}**__ pana la organizarea de Sherpa a lui <@{sherpa}>.
Incepatori: {incepatori}
Experimentati: {experimentati}
Rezerve: {rezerve}'''

    incepatori = ' '.join(['<@{}>'.format(incep[1]) for incep in participants['Beginners']])
    experimentati = ' '.join(['<@{}>'.format(exp[1]) for exp in participants['Experts']])
    rezerve = ' '.join(['<@{}>'.format(rez[1]) for rez in participants['Reserve']])

    out_str = template_string.format(letter=letter, timp=time, sherpa=participants['Sherpa'][1], incepatori=incepatori,
                                     experimentati=experimentati, rezerve=rezerve)
    return out_str


def data_updater(org_old, org_new):
    with open('./sherpa/org_sherpa.json', 'r') as f:
        _temp = json.load(f)

    _temp = _temp['org']
    for _org in _temp:
        if _org == org_old:
            _temp.remove(_org)
            if org_new:
                _temp.append(org_new)

    new_dump = {'org': _temp}

    with open('./sherpa/org_sherpa.json', 'w') as f:
        json.dump(new_dump, f)
