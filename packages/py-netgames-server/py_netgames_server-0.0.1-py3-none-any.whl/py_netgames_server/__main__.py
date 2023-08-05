import argparse
import logging

from py_netgames_server.websocket_server_builder import WebSocketServerBuilder


def setup_logger(log_level):
    logging.basicConfig(format='%(name)s %(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)


def setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Debug websocket connections",
        action="store_const", dest="log_level", const=logging.DEBUG,
        default=logging.ERROR
    )
    parser.add_argument(
        '-p', '--port',
        help="Server port",
        dest="port", default=8765
    )
    return parser


if __name__ == '__main__':
    args = setup_arg_parser().parse_args()
    setup_logger(args.log_level)
    WebSocketServerBuilder().serve(args.port)
