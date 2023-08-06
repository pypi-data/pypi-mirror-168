#######################################
# LaTeX document generator by Pursuit #
#######################################

import argparse
from typing import Sequence

from gentexdoc import PROGRAM_NAME, PROGRAM_VERSION
from gentexdoc.generator import generate_pdf


# The CLI interface of GenTexDoc

def main(args: Sequence[str] = None) -> None:
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-t", "--template", help="specify the template to use", required=True)
    aparser.add_argument("-d", "--define", help="Define a variable", nargs="+")
    aparser.add_argument("input", help="markdown input files", nargs="+")
    aparser.add_argument("-o", "--output", help="specify the output")
    aparser.add_argument("-f", "--force", help="overwrite the output file if it already exists", action="store_true")
    aparser.add_argument("-v", "--verbose", help="display more information about the conversion", action="store_true")
    aparser.add_argument("-V", "--version", help="display the program's version", action="version", version=f"{PROGRAM_NAME} {PROGRAM_VERSION} - by Pursuit")

    args = aparser.parse_args(args)
    context = {}

    if args.define is not None:
        for definition in args.define:
            if "=" not in definition:
                raise Exception("Usage: --define NAME=VALUE")
            equal_pos = definition.index("=")
            name = definition[:equal_pos]
            value = definition[equal_pos+1:]
            if name not in context:
                context[name] = value
            else: print(f"Variable {name} is defined multiple times !")

    success = generate_pdf(args.template, args.input, args.output, args.force, context, args.verbose)
    if not success:
        exit(-1)
