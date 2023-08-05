from setuptools import setup

setup(
    name='nonebot-plugin-chatrecorder-guild-patch',
    version='0.1.2',
    author='MYXS',
    author_email='1964324406@qq.com',
    url='https://github.com/X-Skirt-X/nonebot-plugin-chatrecorder-guild-patch',
    description=u'nonebot-plugin-chatrecorder的频道适配器',
    packages=['nonebot_plugin_chatrecorder_guild_patch'],
    install_requires=[
        'nonebot_plugin_chatrecorder',
        'nonebot_plugin_guild_patch',
        ],
)