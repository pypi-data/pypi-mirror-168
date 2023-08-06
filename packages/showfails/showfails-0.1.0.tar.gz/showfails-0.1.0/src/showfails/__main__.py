import argparse
import logging

from xml.etree import ElementTree as ET


log = logging.getLogger(__name__)


def parse_arguments():
    command_parser = argparse.ArgumentParser()

    command_parser.add_argument(
        "--report-prefix",
        help="save report data to files with the user provided prefix",
        action="store",
        dest="report_prefix",
        default=None,
        type=str)

    command_parser.add_argument(
        "--verbose",
        "-v",
        help="level of logging verbosity",
        default=3,
        action="count",
    )

    command_parser.add_argument(
        "xml_files",
        help="junit style xml files",
        action="store",
        nargs="*",
        type=str)

    # parse options
    options = command_parser.parse_args()

    return options


def list2enumstr(l):
    enumstr = ""
    if len(l) == 0:
        enumstr = "None"
    else:
        for f in enumerate(l):
            enumstr += f"{f[0]}. {f[1]}\n"

    return enumstr.strip()


def main(arguments):

    errors = []
    failures = []
    counts = {
        "errors": 0,
        "fails": 0,
        "tests": 0,
    }

    for infile in arguments.xml_files:
        tree = ET.parse(infile)
        root = tree.getroot()

        testsuite_eles = []
        if root.tag == "testsuite":
            testsuite_eles = [root]
        else:
            testsuite_eles = root.findall(".//testsuite")

        for testsuite in testsuite_eles:
            counts["errors"] += int(testsuite.get("errors"))
            counts["fails"] += int(testsuite.get("failures"))
            counts["tests"] += int(testsuite.get("tests"))

        for testcase in root.findall(".//error/.."):
            class_name = testcase.get("classname")
            test_name = testcase.get("name")
            errors.append(f"{class_name}.{test_name}")

        for testcase in root.findall(".//failure/.."):
            class_name = testcase.get("classname")
            test_name = testcase.get("name")
            failures.append(f"{class_name}.{test_name}")

    error_rate = round(counts["errors"] / counts["tests"] * 100, 2)
    fail_rate = round(counts["fails"] / counts["tests"] * 100, 2)

    enumerated_error_str = list2enumstr(sorted(errors))
    enumerated_failure_str = list2enumstr(sorted(failures))

    report = f"""Failures: {counts['fails']:4.0f}/{counts['tests']} ({fail_rate:.2f}%)
Errors:   {counts['errors']:4.0f}/{counts['tests']} ({error_rate:.2f}%)

FAILURES (failed assertion):
{enumerated_failure_str}

ERRORS (non-assertion exception):
{enumerated_error_str}
"""

    if arguments.report_prefix is None:
        print(report)
    else:
        reportfn = f"{arguments.report_prefix}.report.txt"
        percentfn = f"{arguments.report_prefix}.percent.txt"
        with open(reportfn, "w") as f:
            f.write(report)
        with open(percentfn, "w") as f:
            f.write(f"{fail_rate+error_rate}")


def cli():

    arguments = parse_arguments()

    logging.basicConfig(level=int((6 - arguments.verbose) * 10))

    log.debug(f"arguments = {arguments}")

    main(arguments)

    log.debug("exiting")
