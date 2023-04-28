import discord


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


# Example usage:
permissions_int = 103079233552
permission_strings = permissions_to_str(permissions_int)
print(permission_strings)