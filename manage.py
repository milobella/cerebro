import argparse
import configparser
import logging

from cerebro.server import run

from cerebro.utils import config_to_dict

# Initialize logger
logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)


def runserver_func(arguments: argparse.Namespace):
    logger = logging.getLogger()

    logger.debug("Initialize configuration ...")
    _config = configparser.ConfigParser()
    _config.read_file(arguments.config_file)
    logger.debug("Successfully initialized configuration ! {0}".format(config_to_dict(_config)))

    # Initialize parameters (host and port parameters can be overridden by command line)
    params = {
        "host": _config['server'].get('host') if arguments.host is None else arguments.host,
        "port": _config['server'].getint('port') if arguments.port is None else arguments.port,

        "model": _config["spacy"].get("model", fallback="fr_core_news_md"),
        "iterations": _config["spacy"].getint("iterations", fallback=40),

        "min_score": _config["spacy"].getfloat("min_score", fallback=0.1),
        "chunk_size": _config["spacy"].getint("chunk_size", fallback=1000),

        "use_mongo": _config["features"].getboolean("use_mongo", fallback=False),
        "use_spacy": _config["features"].getboolean("use_spacy", fallback=False),

        "mongo_host": _config["mongodb"].get("host", fallback="0.0.0.0"),
        "mongo_port": _config["mongodb"].getint("port", fallback="27017"),
        "mongo_database": _config["mongodb"].get("database", fallback="cerebro"),
    }

    run(**params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    runserver = subparsers.add_parser("runserver")
    runserver.add_argument("--config-file", type=argparse.FileType('r'), help="Configuration file.")
    runserver.add_argument("--host", type=str, help="The host of the server.")
    runserver.add_argument("--port", type=int, help="The port of the server.")
    runserver.set_defaults(func=runserver_func)
    options = parser.parse_args()

    options.func(options)
