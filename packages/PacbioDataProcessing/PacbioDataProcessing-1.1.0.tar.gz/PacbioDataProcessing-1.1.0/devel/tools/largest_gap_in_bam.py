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

"""This script reports the size of the gaps in the molecule ids (ZMW
numbers) within a BAM file.
"""

import sys
from collections import Counter, defaultdict
import argparse
from pathlib import Path

from pacbio_data_processing.bam import BamFile


HOW_MANY = 10


def parse_cl():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bam", help="BAM file to analyze", type=Path)
    parser.add_argument(
        "-n", "--n-largest-gaps",
        metavar="INT", default=HOW_MANY, type=int,
        help=(
            "how long the output must be (default: print the %(default)s "
            "molecules with the largest gap)"
        )
    )
    return parser.parse_args()


def main():
    args = parse_cl()
    bam = BamFile(args.bam)
    gaps = Counter()
    last_positions = defaultdict(lambda: None)
    for pos, line in enumerate(bam):
        if (pos and (pos % 1_000_000 == 0)):
            print(f"{pos=}", flush=True)
        molid = line.molecule_id
        prev_pos = last_positions[molid]
        if prev_pos:
            gaps[molid] = max(pos-prev_pos, gaps[molid])
        last_positions[molid] = pos
    for molid, gap in gaps.most_common(args.n_largest_gaps):
        print(f"{str(molid)} has a gap of {gap} subreads")


if __name__ == "__main__":
    sys.exit(main())
