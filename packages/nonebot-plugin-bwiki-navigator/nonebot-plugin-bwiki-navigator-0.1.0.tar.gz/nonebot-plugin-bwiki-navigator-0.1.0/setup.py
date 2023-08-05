# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bwiki_navigator']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.20.0,<0.21.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.4,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bwiki-navigator',
    'version': '0.1.0',
    'description': 'A nonebot2 plugin version of bwiki official bot',
    'long_description': '<div align="center">\n\n# nonebot-plugin-bwiki-navigator\n### BWiki助手Nonebot2插件移植版\n\n<a href="https://raw.githubusercontent.com/xzhouqd/nonebot-plugin-bwiki-navigator/main/LICENSE">\n    <img src="https://img.shields.io/github/license/xzhouqd/nonebot-plugin-help?style=for-the-badge" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-bwiki-navigator">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-bwiki-navigator?color=green&style=for-the-badge" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-^3.8-blue?style=for-the-badge" alt="python">\n<br />\n<img src="https://img.shields.io/badge/tested_python-3.10.4-blue?style=for-the-badge" alt="python">\n<img src="https://img.shields.io/static/v1?label=tested+env&message=go-cqhttp+1.0.0-rc3&color=blue&style=for-the-badge" alt="python">\n<br />\n<a href="https://github.com/botuniverse/onebot/blob/master/README.md">\n    <img src="https://img.shields.io/badge/Onebot-v11-brightgreen?style=for-the-badge" alt="onebot">\n</a>\n<a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/static/v1?label=Nonebot&message=^2.0.0%2Dbeta.4&color=red&style=for-the-badge" alt="nonebot">\n</a>\n<a href="https://pypi.org/project/nonebot-adapter-cqhttp/">\n    <img src="https://img.shields.io/static/v1?label=Nonebot-adapters-onebot&message=^2.0.0%2Dbeta.1&color=red&style=for-the-badge" alt="nonebot-adapters-cqhttp">\n</a>\n</div>\n\n## 简介\n本插件是针对BWIKI助手解析的非官方Nonebot2插件移植版\n\n关于BWiki助手解析接入方式，请参阅 [BWIKI - WIKI助手文档](https://wiki.biligame.com/wiki/WIKI%E5%8A%A9%E6%89%8B%E6%96%87%E6%A1%A3)\n\n### 可配置项（可选）\n```\nBWIKI_NAVIGATOR_COMMAND="bwiki"                 // 本插件的主查询命令名\nBWIKI_NAVIGATOR_COMMAND_ALIAS=["wiki"]         // 本插件的查询命令别名列表\n```\n\n### 使用方法\n```\n/bwiki bwiki子站域名 页面名(可选)\n```\n\n### 示例\n```\n/bwiki clover\n\n四叶草剧场WIKI https://wiki.biligame.com/clover\n\n\n/bwiki clover 沙盒\n\n四叶草剧场WIKI 沙盒\nhttps://wiki.biligame.com/clover/?curid=19\n在这里测试你的代码！\n隐藏的wiki bot转换语句\n[图片]\n[图片]\n```\n\n### 已完整接入帮助菜单\n[nonebot-plugin-help](https://github.com/xzhouqd/nonebot-plugin-help) ([PyPI](https://pypi.python.org/pypi/nonebot-plugin-help))',
    'author': 'XZhouQD',
    'author_email': 'X.Zhou.QD@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/XZhouQD/nonebot-plugin-bwiki-navigator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
