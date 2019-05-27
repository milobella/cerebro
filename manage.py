import argparse

from cerebro.server import run


def runserver_func(options):
    run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    runserver = subparsers.add_parser("runserver")
    runserver.add_argument("--host", type=str, help="The host of the server.")
    runserver.add_argument("--port", type=int, help="The port of the server.")
    runserver.set_defaults(func=runserver_func)
    options = parser.parse_args()

    options.func(options)
