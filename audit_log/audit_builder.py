import aiofiles
import discord
import discord.ext

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Functii
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


def compare_changes(before: discord.AuditLogDiff, after: discord.AuditLogDiff):
    differences = {}

    for attr_name, before_value in before.__dict__.items():
        after_value = after.__dict__.get(attr_name, None)
        if before_value != after_value:
            differences[attr_name] = {
                'before': before_value,
                'after': after_value
            }

    return differences


def permissions_to_str(permissions_int: int):
    permissions_obj = discord.Permissions(permissions_int)
    all_permissions = [
        'create_instant_invite',
        'kick_members',
        'ban_members',
        'administrator',
        'manage_channels',
        'manage_guild',
        'add_reactions',
        'view_audit_log',
        'priority_speaker',
        'stream',
        'view_channel',
        'send_messages',
        'send_tts_messages',
        'manage_messages',
        'embed_links',
        'attach_files',
        'read_message_history',
        'mention_everyone',
        'use_external_emojis',
        'view_guild_insights',
        'connect',
        'speak',
        'mute_members',
        'deafen_members',
        'move_members',
        'use_voice_activation',
        'change_nickname',
        'manage_nicknames',
        'manage_roles',
        'manage_webhooks',
        'manage_emojis',
        'request_to_speak',
    ]

    permission_strings = []
    for permission in all_permissions:
        if getattr(permissions_obj, permission):
            permission_strings.append(permission)

    return permission_strings

'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Creare Log
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def prepare_audit(bot: discord.ext.commands.Bot, GUILD_ID, AUDIT_CHANNEL):
    guild = await bot.fetch_guild(GUILD_ID)
    entry_list = []
    new_log_ids = []
    async for entry in guild.audit_logs(limit=25):
        print(entry.action.value, entry.action.name)
        entry_list.append(entry)
        new_log_ids.append(entry.id)

    async with aiofiles.open(r'./audit_log/log_ids.txt', 'r') as f:
        log_ids = await f.read()

    if log_ids:
        int_ids = [int(val) for val in log_ids.split(',')]
        new_events = [ids for ids in entry_list if ids.id not in int_ids]
    else:
        new_events = entry_list

    await class_audit(new_events, bot, GUILD_ID, AUDIT_CHANNEL)

    async with aiofiles.open(r'./audit_log/log_ids.txt', 'w') as f:
        new_event_ids = ','.join([str(i) for i in new_log_ids])
        await f.write(new_event_ids)


async def class_audit(new_events: list, bot: discord.ext.commands.Bot, GUILD_ID, AUDIT_CHANNEL):
    event_dict = {
        'channel': [],
        'permission': [],
        'admin': [],
        'member': [],
        'role': [],
        'message': [],
        'stage': [],
    }

    for event in new_events:
        for remove_type in ['member_move', 'message_pin',
                            'message_unpin']:  # 'automod_', 'webhook_', 'invite_', 'bot_add', 'integration_', 'thread_',
            if remove_type in event.action.name:
                new_events.remove(event)
                continue

        if 'channel_' in event.action.name:
            event_dict['channel'].append(event)
            continue
        if 'overwrite_' in event.action.name:
            event_dict['permission'].append(event)
            continue
        if 'member_' in event.action.name:
            if 'member_move' == event.action.name:
                continue
            event_dict['member'].append(event)
            continue
        if 'role_' in event.action.name:
            event_dict['role'].append(event)
            continue
        if 'message_' in event.action.name:
            if 'message_pin' == event.action.name:
                continue
            if 'message_unpin' == event.action.name:
                continue
            event_dict['message'].append(event)
            continue
        if 'stage_' in event.action.name:
            event_dict['stage'].append(event)
            continue

        if 'ban' in event.action.name or 'unban' in event.action.name or 'kick' in event.action.name or 'member_prune' in event.action.name:
            event_dict['admin'].append(event)
            continue

    print(event_dict)

    await log_builder(event_dict, bot, GUILD_ID, AUDIT_CHANNEL)


async def log_builder(event_dict: dict, bot: discord.ext.commands.Bot, GUILD_ID, AUDIT_CHANNEL):
    # event_dict = {
    #     'channel': [],
    #     'permission': [],
    #     'admin': [],
    #     'member': [],
    #     'role': [],
    #     'message': [],
    #     'stage': [],
    # }
    audit_channel = await bot.fetch_channel(AUDIT_CHANNEL)

    for ch_event in event_dict.get('channel', []):
        await audit_channel.send(embed=ChannelLog(ch_event))
    for per_event in event_dict.get('permission', []):
        await audit_channel.send(embed=PermissionLog(per_event))
    # for admin_event in event_dict.get('admin', []):
    #     await audit_channel.send(embed=AdminLog(admin_event))
    for mem_event in event_dict.get('member', []):
        await audit_channel.send(embed=MemberLog(mem_event))
    for role_event in event_dict.get('role', []):
        await audit_channel.send(embed=RoleLog(role_event))
    # for msg_event in event_dict.get('role', []):
    #     await audit_channel.send(embed=MessageLog(msg_event))
    # for st_event in event_dict.get('stage', []):
    #     await audit_channel.send(embed=StageLog(st_event))


class ChannelLog(discord.Embed):
    def __init__(self, event: discord.AuditLogEntry):
        if '_create' in event.action.name:
            super().__init__(title=f"Channel log",
                             description=f'Canalul <#{event.target.id}> a fost creat!',
                             color=0x347950)
        if '_delete' in event.action.name:
            super().__init__(title=f"Channel log",
                             description=f'Canalul <#{event.target.id}> a fost sters!',
                             color=0xf04848)
        if '_update' in event.action.name:
            super().__init__(title=f"Channel log",
                             description=f'Canalul <#{event.target.id}> a fost modificat!',
                             color=0x347550)
            changes = compare_changes(event.before, event.after)
            for key in changes:
                self.add_field(name=key.title(),
                               value=f'{changes[key]["before"]} —> {changes[key]["after"]}',
                               inline=False)


class PermissionLog(discord.Embed):
    def __init__(self, event: discord.AuditLogEntry):
        if '_create' in event.action.name:
            super().__init__(title=f"Permission log",
                             description=f'Permisiunea <#{event.target.id}> a fost creata!',
                             color=0x347950)
        if '_delete' in event.action.name:
            super().__init__(title=f"Permission log",
                             description=f'Permisiunea <#{event.target.id}> a fost stearsa!',
                             color=0xf04848)
        if '_update' in event.action.name:
            super().__init__(title=f"Permission log",
                             description=f'Permisiunea <#{event.target.id}> a fost modificata!',
                             color=0x347550)
            changes = compare_changes(event.before, event.after)
            for key in changes:
                self.add_field(name=key.title(),
                               value=f'{changes[key]["before"]} —> {changes[key]["after"]}',
                               inline=False)


class MemberLog(discord.Embed):
    def __init__(self, event: discord.AuditLogEntry):
        # if '_create' in event.action.name:
        #     super().__init__(title=f"Member log",
        #                      description=f'Membrul <#{event.target.id}> a fost creat!',
        #                      color=0x347950)
        # if '_delete' in event.action.name:
        #     super().__init__(title=f"Member log",
        #                      description=f'Membrul <#{event.target.id}> a fost stears!',
        #                      color=0xf04848)
        if '_update' in event.action.name:
            super().__init__(title=f"Member log",
                             description=f'Membrul <@{event.target.id}> a fost modificat!',
                             color=0x347550)
            changes = compare_changes(event.before, event.after)
            for key in changes:
                self.add_field(name=key.title(),
                               value=f'{changes[key]["before"]} —> {changes[key]["after"]}',
                               inline=False)
        if '_role_update' in event.action.name:
            super().__init__(title=f"Member log",
                             description=f'Rolul membrului <@{event.target.id}> a fost modificat!',
                             color=0x347550)
            changes = compare_changes(event.before, event.after)
            for key in changes:
                self.add_field(name=key.title(),
                               value=f'{changes[key]["before"]} —> {changes[key]["after"]}',
                               inline=False)

class RoleLog(discord.Embed):
    def __init__(self, event: discord.AuditLogEntry):
        if '_create' in event.action.name:
            super().__init__(title=f"Role log",
                             description=f'Rolul <@&{event.target.id}> a fost creat!',
                             color=0x347950)
        if '_delete' in event.action.name:
            super().__init__(title=f"Role log",
                             description=f'Rolul <@&{event.target.id}> a fost stears!',
                             color=0xf04848)
        if '_update' in event.action.name:
            super().__init__(title=f"Role log",
                             description=f'Rolul <@&{event.target.id}> a fost modificat!',
                             color=0x347550)
            changes = compare_changes(event.before, event.after)
            for key in changes:
                self.add_field(name=key.title(),
                               value=f'{permissions_to_str(changes[key]["before"].value)} —> {permissions_to_str(changes[key]["after"].value)}',
                               inline=False)

# class MessageLog(discord.Embed):
#     def __init__(self, event: discord.AuditLogEntry):
#         if '_create' in event.action.name:
#             super().__init__(title=f"Message log",
#                              description=f'Rolul <#{event.target.id}> a fost creat!',
#                              color=0x347950)
#         if '_delete' in event.action.name:
#             super().__init__(title=f"Message log",
#                              description=f'Rolul <#{event.target.id}> a fost stears!',
#                              color=0xf04848)
#         if '_update' in event.action.name:
#             super().__init__(title=f"Message log",
#                              description=f'Rolul <#{event.target.id}> a fost modificat!',
#                              color=0x347550)
#             changes = compare_changes(event.before, event.after)
#             for key in changes:
#                 self.add_field(name=key.title(),
#                                value=f'{changes[key]["before"]} —> {changes[key]["after"]}',
#                                inline=False)