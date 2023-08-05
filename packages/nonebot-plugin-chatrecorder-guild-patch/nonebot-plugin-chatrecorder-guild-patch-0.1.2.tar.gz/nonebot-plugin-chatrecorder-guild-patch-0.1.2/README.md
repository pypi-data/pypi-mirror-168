# nonebot-plugin-chatrecorder-guild-patch

适用于[nonebot-plugin-chatrecorder](https://github.com/noneplugin/nonebot-plugin-chatrecorder)的频道适配器

### 安装

- 使用 nb-cli

```cmd
nb plugin install nonebot-plugin-chatrecorder-guild-patch
```

- 使用 pip

```cmd
pip install nonebot-plugin-chatrecorder-guild-patch
```

### 配置

插件会记录机器人收到的频道消息

插件依赖 [nonebot-plugin-chatrecorder](https://github.com/noneplugin/nonebot-plugin-chatrecorder) 插件


### 使用

示例：

```python
from datetime import datetime, timedelta
from nonebot_plugin_chatrecorder import get_message_records
from nonebot_plugin_guild_patch import GuildMessageEvent
from nonebot-plugin-chatrecorder-guild-patch import get_guild_all_channel
@matcher.handle()
def handle(event: GuildMessageEvent):
    # 获取当前频道一天内所有子频道的消息
    msgs = await get_message_records(
        group_ids=get_guild_all_channel(event.guild_id),
        time_start=datetime.utcnow() - timedelta(days=1),
    )
```


### 感谢

感谢**大佬MeetWq**写的nonebot-plugin-chatrecorder插件
