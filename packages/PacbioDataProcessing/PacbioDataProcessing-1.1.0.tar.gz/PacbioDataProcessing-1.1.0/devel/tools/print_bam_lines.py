#!/usr/bin/env python

#######################################################################
#
# Copyright (C) 2022 David Palao
#
# This file is part of PacBioDataProcessing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

"""This script prints information about the lines in a BAM file
"""

import sys
from collections import Counter, defaultdict
import argparse
from pathlib import Path

from pacbio_data_processing.bam import BamFile


DEFAULT_INI = 0
DEFAULT_END = -1


def parse_cl():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bam", help="BAM file to analyze", type=Path)
    parser.add_argument(
        "-i", "--initial-line", type=int,
        metavar="INT", default=DEFAULT_INI,
        help="inclusive start; 0-based (default: %(default)s)"
    )
    parser.add_argument(
        "-e", "--final-line", type=int,
        metavar="INT", default=DEFAULT_END,
        help="exclusive end, 0-based (default: end of file)"
    )
    parser.add_argument(
        "--display-line", action="store_true",
        help="display the line itself? (default: %(default)s)"
    )
    parser.add_argument(
        "--display-num-cols", action="store_true",
        help="display how many columns are in the line? (default: %(default)s)"
    )
    return parser.parse_args()


def main():
    args = parse_cl()
    bam = BamFile(args.bam)
    pos0 = args.initial_line
    posN = args.final_line
    for pos, line in enumerate(bam):
        pos_ini_cond = pos >= pos0
        pos_end_cond = True if (posN < 0 or pos < posN) else False
        if pos_ini_cond and pos_end_cond:
            molid = int(line.molecule_id)
            s = f"{molid=}"
            if args.display_num_cols:
                s += f" -> {len(line):>10} columns"
            if args.display_line:
                s += f"\n   line: "+" ".join(str(_) for _ in line) + "\n---\n"
            print(s, flush=True)


if __name__ == "__main__":
    sys.exit(main())
