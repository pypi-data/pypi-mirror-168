import argparse
import logging.config

from erasudy import algorithms
from erasudy.config import settings


# A list of erasure standards available.
# https://en.wikipedia.org/wiki/Data_erasure#Standards
erasure_standard = {
    "Bruce Schneier's Algorithm": algorithms.bruce_schneier,
}


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Erasudy is a tool for securely erasing data.",
    )
    parser.add_argument(
        "-v", "--volume",
        help="The drive to be erased.",
        required=True,
    )
    parser.add_argument(
        "-s", "--standard",
        help="The erasure standard to use.",
        default=settings.default_standard,
        choices=erasure_standard.keys(),
    )
    return parser.parse_args()


def run():
    """Start point for the `erasudy_run` script."""
    args = get_args()
    erasure_standard[args.standard](args.volume)


if __name__ == '__main__':
    logging.config.fileConfig(
        fname='./logging.conf',
        disable_existing_loggers=False,
    )
    # Run for development purposes.
    run()
