#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger, Logger, StreamHandler, Formatter
from pathlib import Path
from importlib import import_module
import logging
import os
import pdb
import sys


LOG = getLogger(__name__)

LOG_LEVEL = logging.INFO

LOGGER_NAME_CANDIDATES = 'logger', '_LOG', 'LOG'


def _import_module():
    sys.path.insert(0, os.getcwd())
    assert len(sys.argv) > 1, sys.argv
    args = sys.argv[1:]
    argv0_path = Path(args[0])
    if len(argv0_path.parts) > 1:
        sys.path.append(str(argv0_path.parent))
    module_name = Path(argv0_path.name).stem
    module = import_module(module_name)
    assert hasattr(module, 'main'), (
            f'{module_name} does not have main()')
    assert hasattr(module, 'add_arguments'), (
            f'{module_name} does not have add_arguments()')
    return module


def _set_loggers(module):
    _set_logger(LOG, LOG_LEVEL)
    module_logger = _get_module_logger(module)
    if module_logger is not None:
        _set_logger(module_logger, LOG_LEVEL)


def _parse_module_arguments(module):
    parser = ArgumentParser(
            prog=sys.argv[1],
            formatter_class=ArgumentDefaultsHelpFormatter)
    module.add_arguments(parser)
    args = parser.parse_args(sys.argv[2:])
    return args


def _get_module_logger(module):
    for c in LOGGER_NAME_CANDIDATES:
        if hasattr(module, c):
            return getattr(module, c)
    LOG.warning(
            f'{module.__name__} does not have any of {LOGGER_NAME_CANDIDATES}')


def _set_logger(logger, level):
    if not isinstance(logger, Logger):
        LOG.warning((
            f'type of logger = {type(logger)} is not logging.Logger.'
            ' do nothing.'))
        return
    __handler = StreamHandler()
    __handler.setLevel(level)
    __handler.setFormatter(Formatter(
        '%(levelname).1s %(asctime)s %(filename)s:%(lineno)d %(message)s'
    ))
    logger.setLevel(level)
    logger.addHandler(__handler)
    logger.propagate = False


def _print_args(args, logger=LOG):
    for k, v in vars(args).items():
        logger.info(f'{k}= {v}')


def _parse_args(add_arguments_func, logger=LOG):
    parser = ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    add_arguments_func(parser)
    args = parser.parse_args()
    return args


def app():
    module = _import_module()
    _set_loggers(module)
    args = _parse_module_arguments(module)
    _print_args(args)
    module.main(args)


_TEMPLATE = '''#!/usr/bin/env python3
from logging import getLogger


logger = getLogger(__name__)


def add_arguments(parser):
    group = parser.add_argument_group(__name__)
    ...


def main(args):
    ...


# code below is an option.
# if you want to run it as an normal Python script
# (`python THIS_SCRIPT.py`), uncomment it.
# if __name__ == '__main__':
#     import wrapp
#     wrapp.main(add_arguments, main, logger)'''


def new():
    print(_TEMPLATE, end='')


def main(add_arguments_func, main_func, logger):
    _set_logger(logger, LOG_LEVEL)
    args = _parse_args(add_arguments_func, logger)
    _print_args(args, logger)
    main_func(args)


if __name__ == '__main__':
    app()
