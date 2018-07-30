#!/usr/bin/env python3

# Native imports
import argparse
import sys

# Installed imports

# Custom imports
from features import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Talk to the GitHub API',
            usage='''github <feature> [<command>]

Available features are:
   pr     Get info about pull requests.
   repo      Get info about repositories.
''')
    parser.add_argument('feature', help='Feature to use')
    args = parser.parse_args(sys.argv[1:2])

    if args.feature not in FEATURES:
        print('Unrecognized feature')
        parser.print_help()
        exit(1)

    FEATURES[args.feature]()




