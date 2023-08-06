# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_selenium', 'pytest_selenium.drivers']

package_data = \
{'': ['*']}

install_requires = \
['pytest-base-url>=2.0.0,<3.0.0',
 'pytest-html>=2.0.0',
 'pytest-variables>=2.0.0,<3.0.0',
 'pytest>=6.0.0,<7.0.0',
 'requests>=2.26.0,<3.0.0',
 'selenium>=4.0.0,<5.0.0',
 'tenacity>=6.0.0,<7.0.0']

extras_require = \
{'appium': ['appium-python-client>=2.0.0,<3.0.0']}

entry_points = \
{'pytest11': ['appium_driver = pytest_selenium.drivers.appium',
              'browserstack_driver = pytest_selenium.drivers.browserstack',
              'chrome_driver = pytest_selenium.drivers.chrome',
              'crossbrowsertesting_driver = '
              'pytest_selenium.drivers.crossbrowsertesting',
              'edge_driver = pytest_selenium.drivers.edge',
              'firefox_driver = pytest_selenium.drivers.firefox',
              'ie_driver = pytest_selenium.drivers.internet_explorer',
              'remote_driver = pytest_selenium.drivers.remote',
              'safari_driver = pytest_selenium.drivers.safari',
              'saucelabs_driver = pytest_selenium.drivers.saucelabs',
              'selenium = pytest_selenium.pytest_selenium',
              'selenium_safety = pytest_selenium.safety',
              'testingbot_driver = pytest_selenium.drivers.testingbot']}

setup_kwargs = {
    'name': 'pytest-selenium',
    'version': '4.0.0',
    'description': 'pytest plugin for Selenium',
    'long_description': 'pytest-selenium\n===============\n\npytest-selenium is a plugin for `pytest <http://pytest.org>`_ that provides\nsupport for running `Selenium <http://seleniumhq.org/>`_ based tests.\n\n.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg\n   :target: https://github.com/pytest-dev/pytest-selenium/blob/master/LICENSE\n   :alt: License\n.. image:: https://img.shields.io/pypi/v/pytest-selenium.svg\n   :target: https://pypi.python.org/pypi/pytest-selenium/\n   :alt: PyPI\n.. image:: https://img.shields.io/travis/pytest-dev/pytest-selenium.svg\n   :target: https://travis-ci.org/pytest-dev/pytest-selenium/\n   :alt: Travis\n.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg\n   :target: http://pytest-selenium.readthedocs.io/en/latest/\n   :alt: Read the Docs\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n.. image:: https://img.shields.io/github/issues-raw/pytest-dev/pytest-selenium.svg\n   :target: https://github.com/pytest-dev/pytest-selenium/issues\n   :alt: Issues\n.. image:: https://img.shields.io/requires/github/pytest-dev/pytest-selenium.svg\n   :target: https://requires.io/github/pytest-dev/pytest-selenium/requirements/?branch=master\n   :alt: Requirements\n\nResources\n---------\n\n- `Documentation <http://pytest-selenium.readthedocs.io/en/latest/>`_\n- `Issue Tracker <http://github.com/pytest-dev/pytest-selenium/issues>`_\n- `Code <http://github.com/pytest-dev/pytest-selenium/>`_\n',
    'author': 'Dave Hunt',
    'author_email': 'dhunt@mozilla.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pytest-dev/pytest-selenium',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
