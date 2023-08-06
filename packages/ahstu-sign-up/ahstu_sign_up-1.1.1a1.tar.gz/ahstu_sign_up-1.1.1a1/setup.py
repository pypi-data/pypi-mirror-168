# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['signup']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8', 'requests>=2.28.1']

entry_points = \
{'console_scripts': ['ahstu_sign_up = signup:main']}

setup_kwargs = {
    'name': 'ahstu-sign-up',
    'version': '1.1.1a1',
    'description': 'a simple script to deal with daily sign-up in AHSTU',
    'long_description': '## 安科填报自动化脚本\n填报过程自动化，适用于安徽科技学院某填报系统，摆脱被班委催填报的尴尬，以造福劳苦大众\n\n- 允许自定义填报信息\n- 支持多人填报（需要相应配置文件）\n- 支持Windows, Linux\n- 与人工填写几经无差别\n\n### 使用方法\n- Windows用户提供一键脚本, 具体使用方法参见 [help.txt](https://github.com/NoSimpleApple/ahstu_sign_up/blob/remote/help.txt) 文件\n- Linux用户需自建python虚拟环境（提供requirements.txt）\n### 使用须知\n1. 以下情况均不负责 \n   - 因使用本脚本而被查处并记过\n   - 因使用本脚本而造成填写内容不为实际信息（有bug在issue提出）\n   - 因使用本脚本而造成本人实质性的损失\n2. 本脚本制作本意仅为方便日常生活，减少重复工作的目的。个人应在保证自身身体健康的情况下使用，积极配合学校防疫工作，时刻检查自身身体情况，若察觉到异常情况，请关停该脚本，认真填写填报信息并上报。\n3. 请低调使用\n',
    'author': 'uncle_hoshino',
    'author_email': 'hgenaaaa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NoSimpleApple/ahstu_sign_up',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
