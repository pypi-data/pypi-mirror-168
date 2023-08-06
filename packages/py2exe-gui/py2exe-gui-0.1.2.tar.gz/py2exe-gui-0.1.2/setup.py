# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py2exe_gui', 'py2exe_gui.Core', 'py2exe_gui.Widgets']

package_data = \
{'': ['*'], 'py2exe_gui': ['Resources/Icons/*']}

install_requires = \
['PySide6>=6.2.0,<6.3.0']

setup_kwargs = {
    'name': 'py2exe-gui',
    'version': '0.1.2',
    'description': 'GUI for PyInstaller, based on PySide6',
    'long_description': '# Py2exe-GUI\n\n> 更易用的 Python 打包工具！\n\n![GitHub Repo stars](https://img.shields.io/github/stars/muziing/Py2exe-GUI)\n[![PyPI Version](https://img.shields.io/pypi/v/py2exe-gui)](https://pypi.org/project/py2exe-gui/)\n[![License](https://img.shields.io/github/license/muziing/Py2exe-GUI)](https://www.gnu.org/licenses/gpl-3.0.html)\n![Python version](https://img.shields.io/pypi/pyversions/py2exe-gui)\n[![PySide Version](https://img.shields.io/badge/PySide-6.2-blue)](https://doc.qt.io/qtforpython/index.html)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## 简介\n\nPy2exe-GUI 是一个基于 [PySide6](https://doc.qt.io/qtforpython/index.html) 开发的 [PyInstaller](https://pyinstaller.org/) 辅助工具，旨在提供完整易用的图形化界面，方便用户进行 Python 项目的打包。\n\n![截图](docs/source/images/Py2exe-GUI_v0.1.0_screenshot.png)\n\n有如下特性：\n\n- 完全图形化界面，易用\n- 支持 PyInstaller 的全部选项\n- 可以调用本地任何一个 Python 解释器，无需在每个待打包的解释器环境中重复安装（暂未实现）\n- 跨平台，Windows、Linux、MacOS 均支持\n\n## 如何使用\n\n### 安装\n\nPy2exe-GUI 已经发布至 PyPI，直接通过 pip 工具安装即可：\n\n```shell\npip install py2exe-gui\n```\n\n### 运行\n\n```shell\npython -m py2exe_gui\n```\n\n## 项目结构\n\n- 项目所有代码均在 [py2exe_gui](src/py2exe_gui) 目录下\n- [Widgets](src/py2exe_gui/Widgets) 目录下包含所有界面控件\n- [Core](src/py2exe_gui/Core) 目录中为执行打包的代码\n\n仅为图形化界面工具，不依赖于需要打包的 Python 环境。也提供 exe 发布版。\n\n可以显式指定打包时使用的 Python 解释器与对应环境\n（调用该解释器的 `python3 -m PyInstaller myscript.py` 即可）\n\n## TODO\n\n- [ ] 解决相对引用与作为包运行问题\n- [x] 选项参数获取\n  - [x] 将参数拼接成完整调用命令\n  - [x] 参数预览器控件\n  - [ ] 优化拼接代码\n- [x] 调用 `PyInstaller` 子进程\n  - [x] 使用 `QProcess` 替代 `subprocess` 以解决界面卡死问题\n  - [x] 将子进程的输出与状态显示至单独的弹出窗口\n  - [ ] 优化子进程相关代码，增强异常处理\n- [ ] 增加主界面功能控件\n  - [ ] Python 解释器选择器\n  - [ ] 增加状态栏信息\n- [ ] 实现跨平台功能（不同平台间的差异功能）\n- [ ] 保存与读取打包项目文件（json? yaml? toml?）\n- [ ] `logging` 日志记录\n- [ ] QSS 与美化\n- [ ] 翻译与国际化\n',
    'author': 'muzing',
    'author_email': 'muzi2001@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/muziing/Py2exe-GUI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
