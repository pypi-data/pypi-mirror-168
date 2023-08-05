# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shimtax', 'shimtax._tests', 'shimtax._tests.encodings']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'click>=8.1.3,<9.0.0', 'setuptools>=52']

extras_require = \
{'build': ['build>=0.5.0', 'twine>=4.0.1,<5.0.0'],
 'checks': ['black>=22.8.0',
            'isort>=5.10.1',
            'mypy>=0.971',
            'pytest>=7.1.3,<8.0.0'],
 'coverage': ['coverage>=6.4.4,<7.0.0'],
 'dev': ['black>=22.8.0',
         'isort>=5.10.1',
         'mypy>=0.971',
         'pytest>=7.1.3,<8.0.0',
         'pytest-cov>=3.0.0,<4.0.0'],
 'test': ['pytest>=7.1.3,<8.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['shimtax = shimtax.cli:main']}

setup_kwargs = {
    'name': 'shimtax',
    'version': '0.1rc1',
    'description': 'A pluggable manager for syntax rewriting codecs',
    'long_description': 'shimtax - a pluggable codec manager for Python syntax modifying encodings\n=========================================================================\n\nYes, this is a joke.  But I think it works?  ``*rofl*``  A joke...  that works...\n\nProjects like `Coconut <http://coconut-lang.org/>`__ and `cursed-for <https://github.com/tusharsadhwani/cursed-for>`__ offer new syntax on top of the standard Python syntax.\nThey achieve this by preprocessing code of their customized form down to standard Python.\nOne option for this preprocessing is to leverage the `source code encoding <https://docs.python.org/3/tutorial/interpreter.html#source-code-encoding>`__ features of Python.\nFor example, specifying ``# coding: coconut``, after some other setup, can enable Coconut syntax for that file.\nBut, what if you need multiple of these syntax modifying encodings?\nThat\'s where shimtax comes in and let\'s you apply multiple other encodings.\n\n..\n   TODO: find a pair that actually work\n\n.. code-block:: python\n\n   # coding: shimtax:cursed-for:coconut\n\n   for (i = 0; i < 10; i += 2):\n       i |> print\n\nGiven that each encoding is offering custom syntax that the others are presumably unaware of, expect many combinations to be order dependent or to simply not work.\nThose that simply operate on the code as a string are much more likely to be mixable.\nThose that parse the code via a Python syntax parser are likely to fail.\n\nSetup\n-----\n\nshimtax can be set to be automatically enabled using the CLI.\nThis will insert a ``.pth`` file in the platlib directory returned by ``sysconfig.get_path("platlib")``.\nThat file will register the shimtax encoding so you don\'t have to.\n\n.. code-block:: console\n\n   $ .venv/bin/shimtax register\n\nThe CLI can also remove the ``.pth`` file.\n\n.. code-block:: console\n\n   $ .venv/bin/shimtax unregister\n\nIf handling this yourself is preferred, you can use the registration helper function.\n\n.. code-block:: python\n\n   import shimtax\n\n   shimtax.register()\n',
    'author': 'Kyle Altendorf',
    'author_email': 'sda@fstab.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/altendky/shimtax/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
