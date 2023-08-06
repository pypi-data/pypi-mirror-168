# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_games',
 'ayaka_games.chengyu',
 'ayaka_games.genshin_dragon',
 'ayaka_games.incan',
 'ayaka_games.template',
 'ayaka_games.utils',
 'ayaka_games.utils.spider']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.2.19,<0.3.0',
 'nonebot2>=2.0.0b5,<3.0.0',
 'pypinyin>=0.47.1,<0.48.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-games',
    'version': '0.0.6',
    'description': 'a pack of textual game on QQ via nonebot-plugin-ayaka',
    'long_description': '# ayaka文字小游戏合集 v0.0.6\n\n基于ayaka开发的文字小游戏合集（共计10个）\n\n<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-games)以获取最新版本的帮助</b>\n\n## 基础插件\n提供金钱管理功能，让游戏更有目的性\n- 背包\n- 签到\n\n## 文字游戏插件\n1. 印加宝藏 [@灯夜](https://github.com/lunexnocty/Meiri)\n2. 原神接龙\n3. 成语接龙\n4. 赌大小\n5. 祈祷nia\n6. 发癫生成器\n7. bingo~\n\n# 更新记录\n\n<details>\n\n<summary>更新记录</summary>\n\n版本 | 备注\n-|-\n0.0.4 | 修复了单个插件错误导致其他插件无法导入的问题\n0.0.5 | 新增插件bingo，checkin，template\n\n</details>\n\n## How to start\n\n首先需要安装 ayaka插件 `poetry add nonebot-plugin-ayaka`\n\n之后安装 `poetry add nonebot-plugin-ayaka-games`\n\n修改nonebot2 在 `bot.py` 中写入 \n\n```python\n# 先加载ayaka\nnonebot.load_plugin("ayaka")\nnonebot.load_plugin("ayaka_games")\n```\n\n## Documentation\n\n前置插件 [nonebot-plugin-ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)\n\n## 特别感谢\n\n[@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
