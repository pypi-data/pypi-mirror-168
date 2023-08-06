# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daypy', 'daypy.plugins']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'daypy',
    'version': '0.2.2',
    'description': '一个日期时间解析器',
    'long_description': '# DayPy\n\n<a href="https://github.com/mic1on/daypy/actions/workflows/test.yml?query=event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/mic1on/daypy/workflows/test%20suite/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://pypi.org/project/daypy" target="_blank">\n    <img src="https://img.shields.io/pypi/v/daypy.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/daypy" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/daypy.svg" alt="Supported Python versions">\n</a>\n\n`daypy`是使用`arrow`为基础，开发的一个插件式的时间解析模块。\n模块的命名及设计模式参考了`dayjs`(JavaScript下的时间处理模块)。\n\n### 安装\n\n```bash\npip install daypy -U\n```\n\n### 示例及文档\n\n[官方文档](https://52caiji.com/posts/other/opensource/daypy.html)',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mic1on/daypy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
