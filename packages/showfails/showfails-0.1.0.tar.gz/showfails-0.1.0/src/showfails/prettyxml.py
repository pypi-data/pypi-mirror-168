import argparse
import logging

from xml.dom import minidom

log = logging.getLogger(__name__)


def parse_arguments():
    command_parser = argparse.ArgumentParser()
    command_parser.add_argument(
        "infile",
        help="input xml file",
        action="store",
        type=str)

    command_parser.add_argument(
        "outfile",
        help="output xml file",
        action="store",
        type=str)

    # parse options
    options = command_parser.parse_args()

    return options


def main(opts):

    with open(opts.infile, "r") as f:
        ugly_xml = f.read()

    parsed_xml = minidom.parseString(ugly_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="   ")

    with open(opts.outfile, "w") as f:
        f.write(pretty_xml)


def cli():

    # parse the command line options
    opts = parse_arguments()

    logging.basicConfig(level=int((6 - opts.verbose) * 10))

    log.debug("opts = {}".format(opts))

    main(opts)

    log.debug("exiting")


if __name__ == "__main__":

    cli()
