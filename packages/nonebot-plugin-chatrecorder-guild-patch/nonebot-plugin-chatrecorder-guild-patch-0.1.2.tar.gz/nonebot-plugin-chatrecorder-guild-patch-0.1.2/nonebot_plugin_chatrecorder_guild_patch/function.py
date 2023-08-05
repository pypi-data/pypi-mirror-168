from nonebot.adapters import Bot

async def get_guild_all_channel(guild_id, bot:Bot, no_cache=True):
    datas = await bot.call_api("get_guild_channel_list", guild_id = guild_id, no_cache = no_cache)
    result = []
    for i in datas:
        result.append(i['owner_guild_id']+'_'+i['channel_id'])
    return result