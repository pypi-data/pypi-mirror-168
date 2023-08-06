# wrapp: Making a CLI Application by wrapping


## INSTALL

```
pip install wrapp
```

## USAGE

### TL;DR

1. Create your Python script under a few rules. To do so, start with `wrapp.new`.

    ```
    wrapp.new > YOURS.py
    ```

2. Edit `YOURS.py` as you like.

3. Then you can run your Python script as an CLI app.

    ```
    wrapp YOURS.py
    ```

That's it. Let's enjoy !


### Create your Python script under a few rules

By using `wrapp.new`,

```
wrapp.new > YOURS.py
```

you can get a template Python file named `YOURS.py`.


`wrapp.new` outputs template code at stdout.

```
$ cat YOURS.py
#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    ...


def main(args):
    ...


# code below is an option.
# if you want to run it as an normal Python script
# (`python THIS_SCRIPT.py`), uncomment it.
# if __name__ == '__main__':
#     import wrapp
#     wrapp.main(add_arguments, main, logger)
```

Starting with this template, add program options in `add_arguments(parser)`.  
The type of `parser` is assumed as `argparse.ArgumentParser` class.

And `main(args)` function is the entry point.
When you run `wrapp YOURS.py`, the program arguments are parsed as defined in `add_arguments(parser)` and stored in the variable named `args`.
Then all program arguments and options are output via `logger`.
Finally, the `main(args)` is called.

As shown above, wrapp assumes your Python file contains `add_arguments(parser)` and `main(args)`.
`logger` is optional. Also `logger` can be replaced its name as `_LOG` or `LOG`.
For `logger`, it's OK to use any other 3rd-party logging modules like [`loguru`](https://github.com/Delgan/loguru).


### Run your Python script as an CLI app

Assume your Python script is `YOURS.py`.

```
wrapp YOURS.py --your-options ...
```

That is, just replace `python` to `wrapp`.
Then you can keep your script simple:

- `if __name__ == '__main__':` is not needed.
- Also you don't need any noisy modules such as `argparse`, `from argparse import ...`, `from logging import ...`.


### "I want to run it as `python my_script.py`"

If you want to run your code as an usual Python way, just uncomment last 3 lines of the template.

Then you can run like

```
python my_script.py --some-option ...
```


### Debugging

When you want to debug your script, run the code like this.

```
python3 -m pdb -m wrapp YOURS.py --your-options ...
```

Then the debugging mode (`pdb`) will be started.


## FEATURES

- No dependencies. wrapp only depends on Python standard libraries.
- One file. If you don't need to install other packages at all, just copy `src/wrapp/wrapp.py`.

    ```
    $ cp PATH/TO/wrapp_repo/src/wrapp/wrapp.py ./wrapp
    $ chmod u+x wrapp
    $ ./wrapp.new > YOURS.py
    $ ./wrapp YOURS.py
    ```

- It's like [python-fire](https://github.com/google/python-fire). But for wrapp, you don't need to import any other module in your Python code.
- It's trivial but you also run your script without the extension; `wrapp YOURS`.


## LICENSE

MIT License.


## BACKGROUNDS

As I wrote tons of Python CLI applications, I noticed that,

- `argparse` is the best practice to add my program command options.
- `logging` is not bad if I modify something (format, ...).
- But I noticed that there are many similar lines in my applications. And they make my code more dirty.

Here is my application code pattern. Please note that there is nothing infomative.

```
#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger
from pathlib import Path
import logging.config


_LOG = getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
            'in_file', type=Path,
            help='An input file.')
    parser.add_argument(
            '--out-dir', '-d', type=Path, default=None,
            help='A directory.')


def _main(args):
    _LOG.debug('debug')
    _LOG.info('info')
    _LOG.warning('warning')
    _LOG.error('error')
    _LOG.critical('critical')
    ...


def _parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input-files', nargs='*', help='input files.')
    args = parser.parse_args()
    logging.config.fileConfig('logging.conf')
    for k,v in vars(args).items():
        _LOG.info('{}= {}'.format(k, v))
    return args


def _print_args(args):
    for k, v in vars(args).items():
        _LOG.info(f'{k}= {v}')


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    add_arguments(parser)
    args = parser.parse_args()
    logging.config.fileConfig('logging.conf')
    _print_args(args)
    _main(args)
```

So I decided to separate it to 2 files; one is the contents only and the other is a wrappter to make any Python files an CLI app.

Finally, I can make the above code much more simple,

```
#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path


_LOG = getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
            'in_file', type=Path,
            help='An input file.')
    parser.add_argument(
            '--out-dir', '-d', type=Path, default=None,
            help='A directory.')


def main(args):
    _LOG.debug('debug')
    _LOG.info('info')
    _LOG.warning('warning')
    _LOG.error('error')
    _LOG.critical('critical')
    ...
```

It's similar to [python-fire](https://github.com/google/python-fire).

But when I used the fire, I have to insert `from fire import Fire` and `Fire(your_func)`. I'd like to remove even such a few code.

Then I'm completly free from noisy modules / code !
