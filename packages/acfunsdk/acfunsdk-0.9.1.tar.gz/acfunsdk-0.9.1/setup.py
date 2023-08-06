# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acfunsdk', 'acfunsdk.page']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5', 'httpx>=0.23,<0.24', 'lxml>=4,<5']

setup_kwargs = {
    'name': 'acfunsdk',
    'version': '0.9.1',
    'description': 'acfunsdk - UNOFFICEICAL',
    'long_description': '# acfunsdk - **UNOFFICEICAL**\n\n<br />\n\n<p align="center">\n<a href="https://github.com/dolaCmeo/acfunsdk">\n<img height="100" src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg" alt="">\n<img height="100" src="https://ali-imgs.acfun.cn/kos/nlav10360/static/common/widget/header/img/acfunlogo.11a9841251f31e1a3316.svg" alt="">\n</a>\n</p>\n\n<br />\n\nacfunsdk是 **非官方的 [AcFun弹幕视频网][acfun.cn]** Python库。\n\n> 声明：`acfunsdk`是python的学习工具，并未破解任何acfun相关内容。代码完全公开，仅用于交流学习。\n> 如涉及版权等相关问题，请遵守acfun相关协议及法律法规。如有bug或其他疑问，欢迎发布[issues][Issue]。\n\n- - -\n\n**Python** : `Python>=3.7`， 本体请自行[下载安装][python]。\n\n## [从PyPI安装](https://pypi.org/project/acfunsdk/)\n\n```shell\npython -m pip install acfunsdk\n```\n\n- - -\n\n## 使用方法\n\n\n### 实例化获取对象\n```python\nfrom acfunsdk import Acer\n# 实例化一个Acer\nacer = Acer(debug=True)\n# 登录用户(成功登录后会自动保存 \'<用户名>.cookies\')\n# 请注意保存，防止被盗\nacer.login(username=\'you@email.com\', password=\'balalabalala\')\n# 读取用户(读取成功登录后保存的 \'<用户名>.cookies\')\nacer.loading(username=\'13800138000\')\n# 每日签到，领香蕉🍌\nacer.signin()\n# 通过链接直接获取内容对象\n# 目前支持 9种内容类型：\n# 视  频: https://www.acfun.cn/v/ac4741185\ndemo_video = acer.get("https://www.acfun.cn/v/ac4741185")\nprint(demo_video)\n# 文  章: https://www.acfun.cn/a/ac16695813\ndemo_article = acer.get("https://www.acfun.cn/a/ac16695813")\nprint(demo_article)\n# 合  集: https://www.acfun.cn/a/aa6001205\ndemo_album = acer.get("https://www.acfun.cn/a/aa6001205")\nprint(demo_album)\n# 番  剧: https://www.acfun.cn/bangumi/aa5023295\ndemo_bangumi = acer.get("https://www.acfun.cn/bangumi/aa5023295")\nprint(demo_bangumi)\n# 个人页: https://www.acfun.cn/u/39088\ndemo_up = acer.get("https://www.acfun.cn/u/39088")\nprint(demo_up)\n# 动  态: https://www.acfun.cn/moment/am2797962\ndemo_moment = acer.get("https://www.acfun.cn/moment/am2797962")\nprint(demo_moment)\n# 直  播: https://live.acfun.cn/live/378269\ndemo_live = acer.get("https://live.acfun.cn/live/378269")\nprint(demo_live)\n# 分  享: https://m.acfun.cn/v/?ac=37086357\ndemo_share = acer.get("https://m.acfun.cn/v/?ac=37086357")\nprint(demo_share)\n# 涂鸦(单页): https://hd.acfun.cn/doodle/knNWmnco.html\ndemo_doodle = acer.get("https://hd.acfun.cn/doodle/knNWmnco.html")\nprint(demo_doodle)\n```\n\n- - -\n\n\n<details>\n<summary>依赖库</summary>\n\n**依赖: 包含在 `requirements.txt` 中**\n\n+ [`httpx`](https://pypi.org/project/httpx/)`>=0.23`\n+ [`lxml`](https://pypi.org/project/lxml/)`>=4`\n+ [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)`>=4`\n\n</details>\n\n- - - \n## 参考 & 鸣谢\n\n+ [AcFun 助手](https://github.com/niuchaobo/acfun-helper) 是一个适用于 AcFun（ acfun.cn ） 的浏览器插件。\n+ [AcFunDanmaku](https://github.com/wpscott/AcFunDanmaku) 是用C# 和 .Net 6编写的AcFun直播弹幕工具。\n+ [实现自己的AcFun直播弹幕姬](https://www.acfun.cn/a/ac16695813) [@財布士醬](https://www.acfun.cn/u/311509)\n+ QQ频道“AcFun开源⑨课”\n+ 使用 [Poetry](https://python-poetry.org/) 构建\n\n- - - \n\n## About Me\n\n[![ac彩娘-阿部高和](https://tx-free-imgs2.acfun.cn/kimg/bs2/zt-image-host/ChQwODliOGVhYzRjMTBmOGM0ZWY1ZRCIzNcv.gif)][dolacfun]\n[♂ 整点大香蕉🍌][acfunsdk_page]\n<img alt="AcFunCard" align="right" src="https://discovery.sunness.dev/39088">\n\n- - - \n\n[dolacfun]: https://www.acfun.cn/u/39088\n[acfunsdk_page]: https://www.acfun.cn/a/ac37416587\n\n[acfun.cn]: https://www.acfun.cn/\n[Issue]: https://github.com/dolaCmeo/acfunsdk/issues\n[python]: https://www.python.org/downloads/\n[venv]: https://docs.python.org/zh-cn/3.8/library/venv.html\n\n[acer]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/acer_demo.py\n[index]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/index_reader.py\n[channel]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/channel_reader.py\n[search]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/seach_reader.py\n\n[bangumi]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/bangumi_demo.py\n[video]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/video_demo.py\n[article]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/article_demo.py\n[album]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/album_demo.py\n[member]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/member_demo.py\n[moment]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/moment_demo.py\n[live]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/live_demo.py\n\n[saver]: https://github.com/dolaCmeo/acfunsdk/blob/main/examples/AcSaver_demo.py\n',
    'author': 'dolacmeo',
    'author_email': 'dolacmeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/acfunsdk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
