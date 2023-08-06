# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wrapp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wrapp = wrapp.wrapp:app', 'wrapp.new = wrapp.wrapp:new']}

setup_kwargs = {
    'name': 'wrapp',
    'version': '0.4.3',
    'description': 'Making a CLI Application by wrapping',
    'long_description': '# wrapp: Making a CLI Application by wrapping\n\n\n## INSTALL\n\n```\npip install wrapp\n```\n\n## USAGE\n\n### TL;DR\n\n1. Create your Python script under a few rules. To do so, start with `wrapp.new`.\n\n    ```\n    wrapp.new > YOURS.py\n    ```\n\n2. Edit `YOURS.py` as you like.\n\n3. Then you can run your Python script as an CLI app.\n\n    ```\n    wrapp YOURS.py\n    ```\n\nThat\'s it. Let\'s enjoy !\n\n\n### Create your Python script under a few rules\n\nBy using `wrapp.new`,\n\n```\nwrapp.new > YOURS.py\n```\n\nyou can get a template Python file named `YOURS.py`.\n\n\n`wrapp.new` outputs template code at stdout.\n\n```\n$ cat YOURS.py\n#!/usr/bin/env python3\nfrom logging import getLogger\n\n\nlogger = getLogger(__name__)\n\n\ndef add_arguments(parser):\n    ...\n\n\ndef main(args):\n    ...\n\n\n# code below is an option.\n# if you want to run it as an normal Python script\n# (`python THIS_SCRIPT.py`), uncomment it.\n# if __name__ == \'__main__\':\n#     import wrapp\n#     wrapp.main(add_arguments, main, logger)\n```\n\nStarting with this template, add program options in `add_arguments(parser)`.  \nThe type of `parser` is assumed as `argparse.ArgumentParser` class.\n\nAnd `main(args)` function is the entry point.\nWhen you run `wrapp YOURS.py`, the program arguments are parsed as defined in `add_arguments(parser)` and stored in the variable named `args`.\nThen all program arguments and options are output via `logger`.\nFinally, the `main(args)` is called.\n\nAs shown above, wrapp assumes your Python file contains `add_arguments(parser)` and `main(args)`.\n`logger` is optional. Also `logger` can be replaced its name as `_LOG` or `LOG`.\nFor `logger`, it\'s OK to use any other 3rd-party logging modules like [`loguru`](https://github.com/Delgan/loguru).\n\n\n### Run your Python script as an CLI app\n\nAssume your Python script is `YOURS.py`.\n\n```\nwrapp YOURS.py --your-options ...\n```\n\nThat is, just replace `python` to `wrapp`.\nThen you can keep your script simple:\n\n- `if __name__ == \'__main__\':` is not needed.\n- Also you don\'t need any noisy modules such as `argparse`, `from argparse import ...`, `from logging import ...`.\n\n\n### "I want to run it as `python my_script.py`"\n\nIf you want to run your code as an usual Python way, just uncomment last 3 lines of the template.\n\nThen you can run like\n\n```\npython my_script.py --some-option ...\n```\n\n\n### Debugging\n\nWhen you want to debug your script, run the code like this.\n\n```\npython3 -m pdb -m wrapp YOURS.py --your-options ...\n```\n\nThen the debugging mode (`pdb`) will be started.\n\n\n## FEATURES\n\n- No dependencies. wrapp only depends on Python standard libraries.\n- One file. If you don\'t need to install other packages at all, just copy `src/wrapp/wrapp.py`.\n\n    ```\n    $ cp PATH/TO/wrapp_repo/src/wrapp/wrapp.py ./wrapp\n    $ chmod u+x wrapp\n    $ ./wrapp.new > YOURS.py\n    $ ./wrapp YOURS.py\n    ```\n\n- It\'s like [python-fire](https://github.com/google/python-fire). But for wrapp, you don\'t need to import any other module in your Python code.\n- It\'s trivial but you also run your script without the extension; `wrapp YOURS`.\n\n\n## LICENSE\n\nMIT License.\n\n\n## BACKGROUNDS\n\nAs I wrote tons of Python CLI applications, I noticed that,\n\n- `argparse` is the best practice to add my program command options.\n- `logging` is not bad if I modify something (format, ...).\n- But I noticed that there are many similar lines in my applications. And they make my code more dirty.\n\nHere is my application code pattern. Please note that there is nothing infomative.\n\n```\n#!/usr/bin/env python3\nfrom argparse import ArgumentParser, ArgumentDefaultsHelpFormatter\nfrom logging import getLogger\nfrom pathlib import Path\nimport logging.config\n\n\n_LOG = getLogger(__name__)\n\n\ndef add_arguments(parser):\n    parser.add_argument(\n            \'in_file\', type=Path,\n            help=\'An input file.\')\n    parser.add_argument(\n            \'--out-dir\', \'-d\', type=Path, default=None,\n            help=\'A directory.\')\n\n\ndef _main(args):\n    _LOG.debug(\'debug\')\n    _LOG.info(\'info\')\n    _LOG.warning(\'warning\')\n    _LOG.error(\'error\')\n    _LOG.critical(\'critical\')\n    ...\n\n\ndef _parse_args():\n    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)\n    parser.add_argument(\'-i\', \'--input-files\', nargs=\'*\', help=\'input files.\')\n    args = parser.parse_args()\n    logging.config.fileConfig(\'logging.conf\')\n    for k,v in vars(args).items():\n        _LOG.info(\'{}= {}\'.format(k, v))\n    return args\n\n\ndef _print_args(args):\n    for k, v in vars(args).items():\n        _LOG.info(f\'{k}= {v}\')\n\n\nif __name__ == \'__main__\':\n    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)\n    add_arguments(parser)\n    args = parser.parse_args()\n    logging.config.fileConfig(\'logging.conf\')\n    _print_args(args)\n    _main(args)\n```\n\nSo I decided to separate it to 2 files; one is the contents only and the other is a wrappter to make any Python files an CLI app.\n\nFinally, I can make the above code much more simple,\n\n```\n#!/usr/bin/env python3\nfrom logging import getLogger\nfrom pathlib import Path\n\n\n_LOG = getLogger(__name__)\n\n\ndef add_arguments(parser):\n    parser.add_argument(\n            \'in_file\', type=Path,\n            help=\'An input file.\')\n    parser.add_argument(\n            \'--out-dir\', \'-d\', type=Path, default=None,\n            help=\'A directory.\')\n\n\ndef main(args):\n    _LOG.debug(\'debug\')\n    _LOG.info(\'info\')\n    _LOG.warning(\'warning\')\n    _LOG.error(\'error\')\n    _LOG.critical(\'critical\')\n    ...\n```\n\nIt\'s similar to [python-fire](https://github.com/google/python-fire).\n\nBut when I used the fire, I have to insert `from fire import Fire` and `Fire(your_func)`. I\'d like to remove even such a few code.\n\nThen I\'m completly free from noisy modules / code !\n',
    'author': 'Taro W',
    'author_email': '19923207+t-aro-w@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
