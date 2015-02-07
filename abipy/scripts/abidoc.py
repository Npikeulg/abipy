#!/usr/bin/env python
"""
Interface to the database of ABINIT input variables
"""
from __future__ import print_function, division, unicode_literals

import sys
import os
import argparse

from pprint import pprint
from abipy.abilab import abinit_help
from abipy.htc.abivars_db import get_abinit_variables


def print_vlist(vlist, options):
    for v in vlist:
        print(repr(v))

    if options.verbose:
        for v in vlist: abinit_help(v)
    else:
        print("\nUse -v for more info")


def main():
    def str_examples():
        examples = """\
Usage example:
    abidoc.py man ecut      --> Show documentation for ecut input variable.
    abidoc.py apropos ecut  --> To search in the database for the variables related to ecut.
    abidoc.py find paw      --> To search in the database for the variables whose name contains paw 
    abidoc.py list          --> Print full list of variables 
"""
        return examples

    def show_examples_and_exit(err_msg=None, error_code=1):
        """Display the usage of the script."""
        sys.stderr.write(str_examples())
        if err_msg: sys.stderr.write("Fatal Error\n" + err_msg + "\n")
        sys.exit(error_code)

    # Build the main parser.
    parser = argparse.ArgumentParser(epilog=str_examples(), formatter_class=argparse.RawDescriptionHelpFormatter)

    base_parser = argparse.ArgumentParser(add_help=False)

    base_parser.add_argument('-v', '--verbose', default=0, action='count', # -vv --> verbose=2
                        help='verbose, can be supplied multiple times to increase verbosity')

    base_parser.add_argument('varname', help="ABINIT variable")

    # Create the parsers for the sub-commands
    subparsers = parser.add_subparsers(dest='command', help='sub-command help', description="Valid subcommands")

    # Subparser for man.
    p_man = subparsers.add_parser('man', parents=[base_parser], help="Show documentation for varname.")

    # Subparser for apropos.
    p_apropos = subparsers.add_parser('apropos', parents=[base_parser], help="Find variables related to varname.")

    # Subparser for find.
    p_find = subparsers.add_parser('find', parents=[base_parser], help="Find all variables whose name contains varname.")

    # Subparser for require.
    #p_require = subparsers.add_parser('require', parents=[base_parser], help="Find all variables required by varname.")

    # Subparser for exclude.
    #p_exclude = subparsers.add_parser('exclude', parents=[base_parser], help="Find all variables exclude by varname.")

    # Subparser for list.
    p_list = subparsers.add_parser('list', help="List all variables.")

    try:
        options = parser.parse_args()
    except Exception as exc: 
        show_examples_and_exit(error_code=1)

    database = get_abinit_variables()

    if options.command == "man":
        varname = options.varname
        abinit_help(varname)
        var = database[varname]
        print(var.info)

    elif options.command == "apropos":
        varname = options.varname
        vlist = database.apropos(varname)
        print("apropos results:\n")
        print_vlist(vlist, options)

    elif options.command == "find":
        varname = options.varname
        vlist = [v for v in database.values() if varname in v.varname]
        print("find results:\n")
        print_vlist(vlist, options)

    #elif options.command == "require":
    #    vlist = database.require(varname)
    #    print_vlist(vlist, options)

    #elif options.command == "exclude":
    #    vlist = database.exclude(varname)
    #    print_vlist(vlist, options)

    elif options.command == "list":
        for i, var in enumerate(database.values()):
            print(i, repr(var))

    else:
        raise ValueError("Don't know how to handle command %s" % options.command)


if __name__ == "__main__":
    try:
        do_prof = sys.argv[1] == "prof"
        if do_prof: sys.argv.pop(1)
    except: 
        do_prof = False

    if do_prof:
        import pstats, cProfile
        cProfile.runctx("main()", globals(), locals(), "Profile.prof")
        s = pstats.Stats("Profile.prof")
        s.strip_dirs().sort_stats("time").print_stats()
    else:
        sys.exit(main())
