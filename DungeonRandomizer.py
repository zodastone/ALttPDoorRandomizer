#!/usr/bin/env python3
import argparse
import copy
import os
import logging
import random
import textwrap
import shlex
import sys

from CLI import parse_arguments
from Main import main
from Rom import get_sprite_from_name
from Utils import is_bundled, close_console
from Fill import FillError

def start():
    args = parse_arguments(None)

    if is_bundled() and len(sys.argv) == 1:
        # for the bundled builds, if we have no arguments, the user
        # probably wants the gui. Users of the bundled build who want the command line
        # interface shouuld specify at least one option, possibly setting a value to a
        # default if they like all the defaults
        from Gui import guiMain
        close_console()
        guiMain()
        sys.exit(0)

    # ToDo: Validate files further than mere existance
    if not args.jsonout and not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        sys.exit(1)
    if any([sprite is not None and not os.path.isfile(sprite) and not get_sprite_from_name(sprite) for sprite in args.sprite.values()]):
        if not args.jsonout:
            input('Could not find link sprite sheet at given location. \nPress Enter to exit.')
            sys.exit(1)
        else:
            raise IOError('Cannot find sprite file at %s' % args.sprite)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.gui:
        from Gui import guiMain
        guiMain(args)
    elif args.count is not None:
        seed = args.seed or random.randint(0, 999999999)
        failures = []
        logger = logging.getLogger('')
        for _ in range(args.count):
            try:
                main(seed=seed, args=args)
                logger.info('Finished run %s', _+1)
            except (FillError, Exception, RuntimeError) as err:
                failures.append((err, seed))
                logger.warning('Generation failed: %s', err)
            seed = random.randint(0, 999999999)
        for fail in failures:
            logger.info('%s seed failed with: %s', fail[1], fail[0])
        fail_rate = 100 * len(failures) / args.count
        success_rate = 100 * (args.count - len(failures)) / args.count
        fail_rate = str(fail_rate).split('.')
        success_rate = str(success_rate).split('.')
        logger.info('Generation fail    rate: ' + str(fail_rate[0]   ).rjust(3, " ") + '.' + str(fail_rate[1]   ).ljust(6, '0') + '%')
        logger.info('Generation success rate: ' + str(success_rate[0]).rjust(3, " ") + '.' + str(success_rate[1]).ljust(6, '0') + '%')
    else:
        main(seed=args.seed, args=args)


if __name__ == '__main__':
    start()
