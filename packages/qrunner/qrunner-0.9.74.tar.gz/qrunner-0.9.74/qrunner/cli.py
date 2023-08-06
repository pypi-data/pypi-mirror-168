import argparse
import sys
from qrunner import __version__, __description__
from qrunner.scaffold import init_scaffold_project, main_scaffold_project


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version",
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_project = init_scaffold_project(subparsers)

    if len(sys.argv) == 1:
        # qrunner
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version", "-v"]:
            # qrunner -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # qrunner -h
            parser.print_help()
        elif sys.argv[1] == "start":
            # qrunner startpro
            main_scaffold_project()
        sys.exit(0)


if __name__ == "__main__":
    main()
