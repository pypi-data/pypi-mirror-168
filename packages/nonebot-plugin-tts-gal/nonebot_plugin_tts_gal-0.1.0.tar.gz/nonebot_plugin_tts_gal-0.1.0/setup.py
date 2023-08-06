# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_tts_gal',
 'nonebot_plugin_tts_gal.monotonic_align',
 'nonebot_plugin_tts_gal.text']

package_data = \
{'': ['*']}

install_requires = \
['ffmpy>=0.3.0,<0.4.0',
 'jamo>=0.4.1,<0.5.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'numba>=0.56.0,<0.57.0',
 'numpy>=1.18.5,<2.0.0',
 'pyopenjtalk>=0.2.0,<0.3.0',
 'scipy>=1.5.2,<2.0.0',
 'torch>=1.6.0,<2.0.0',
 'unidecode>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-tts-gal',
    'version': '0.1.0',
    'description': '',
    'long_description': '\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n  \n# nonebot_plugin_tts_gal\n\n基于nonebot和vits的部分gal角色的语音合成插件\n\n</div>\n\n\n\n# 前言\n\n本人python比较菜，因此可能有些地方写的比较屎，还望轻喷\n\n# 安装\n\npip安装\n\n```\npip install nonebot_plugin_tts_gal\n```\n\nnb-cli安装\n\n```\nnb plugin install nonebot-plugin-tts-gal\n```\n\n\n\n## 资源文件\n\n下载`data`文件夹，并放入在bot的运行目录下\n\n\n\n## 相关依赖\n\nffmpeg的安装\n\n#### Windows\n\n在ffmpeg官网下载[ffmpeg下载](https://github.com/BtbN/FFmpeg-Builds/releases),选择对应的版本，下载后解压，并将位于`bin`目录添加到环境变量中\n\n其他具体细节可自行搜索\n\n#### Linux\n\nUbuntu下\n\n```\napt-get install ffmpeg\n```\n\n或者下载源码安装(具体可搜索相关教程)\n\n# 配置项\n\n请在使用的配置文件(.env.*)加入\n\n```\nauto_delete_voice = True\n```\n\n用于是否自动删除生成的语音文件，如不想删除，可改为\n\n```\nauto_delete_voice = False\n```\n\n\n\n# 使用\n\n群聊和私聊仅有细微差别，其中下面语句中，`name`为合成语音的角色，`text`为转语音的文本内容(会自动转为日文，故也可以输入中文等其他语言)\n\n## 群聊\n\n`@机器人 [name]说[text]`\n\n## 私聊\n\n`[name]说[text]`\n\n\n\n目前`name`有\n\n- 宁宁|绫地宁宁\n- 因幡爱瑠|爱瑠\n- 朝武芳乃|芳乃\n- 常陸茉子|茉子\n- 丛雨|幼刀\n- 鞍馬小春|鞍马小春|小春\n- 在原七海|七海\n- ATRI|atri|亚托莉\n\n\n\n# 今后\n\n添加更多的模型\n\n\n\n# 感谢\n\n+ 部分代码参考自[nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet)\n\n+ **[CjangCjengh](https://github.com/CjangCjengh/)**：g2p转换，适用于日语调形标注的符号文件及分享的[柚子社多人模型](https://github.com/CjangCjengh/TTSModels)\n+ **[luoyily](https://github.com/luoyily)**：分享的[ATRI模型](https://pan.baidu.com/s/1_vhOx50OE5R4bE02ZMe9GA?pwd=9jo4)\n',
    'author': 'dpm12345',
    'author_email': '1006975692@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dpm12345/nonebot_plugin_tts_gal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
