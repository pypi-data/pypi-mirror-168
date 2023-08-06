# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seletrans', 'seletrans.api', 'seletrans.constants']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'chromedriver-autoinstaller>=0.3.1,<0.4.0',
 'pytest>=7.1.2,<8.0.0',
 'selenium>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'seletrans',
    'version': '0.4.1',
    'description': 'Translate phase using selenium.',
    'long_description': '# SeleTrans\n\nTranslate phase using selenium. And you can also play the sound of the phase you are querying.\n\nCurrently support `Baidu`, `DeepL` and `Google`.\n\n## Usage\n\n```python\nfrom seletrans.api import *\n\nwith Google() as ts:\n    res = ts.query("book", target="zh-CN")\n    print(res.result)\n    print(res.dict_result)\n    res.play_sound()\n```\n\nCheck the test case for more information, or run it yourself to see the results.\n\n## Explain\n\nWhy use selenium? Why not use requests?\n\nAlthough selenium is slower than requests, it is more convenient to adapt when API changes.\n\n## Notice\nOn the mac, you have to run `/Applications/Python 3.10/Install Certificates.command` to avoid \n\n```\nurllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)>\n```\n',
    'author': 'SErAphLi',
    'author_email': 'seraphlivery@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
