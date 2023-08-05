from datetime import datetime

from nonebot import  require
from nonebot.message import event_postprocessor

require("nonebot_plugin_datastore")
from nonebot_plugin_datastore import create_session
require("nonebot_plugin_chatrecorder")
from nonebot_plugin_chatrecorder import serialize_message
from nonebot_plugin_chatrecorder.model import MessageRecord
require("nonebot_plugin_guild_patch")
from nonebot_plugin_guild_patch import GuildMessageEvent

from .function import get_guild_all_channel

@event_postprocessor
async def record_recv_msg(event: GuildMessageEvent):
    
    record = MessageRecord(
        platform="qq_guild",
        time=datetime.utcfromtimestamp(event.time),
        type="message",
        detail_type="group",
        message_id=str(event.message_id),
        message=serialize_message(event.message),
        alt_message=event.message.extract_plain_text(),
        user_id=str(event.user_id),
        group_id=str(event.guild_id)+'_'+str(event.channel_id),  #便于区分子频道和主频道
    )

    async with create_session() as session:
        session.add(record)
        await session.commit()
        
