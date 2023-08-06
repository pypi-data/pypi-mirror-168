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
"""A module containing methylation related code.
"""

from pathlib import Path
import logging
import csv
from itertools import groupby
from statistics import mean
from collections import defaultdict, Counter

from .utils import combine_scores


METHYLATION_REPORT_HEADER = [
    "molecule id", "sequence", "start of molecule", "end of molecule",
    "len(molecule)", "count(subreads+)", "count(subreads-)",
    "combined QUAL", "mean(QUAL)", "sim ratio",
    "count(GATC)", "positions of GATCs",
    "count(methylation states)", "methylation states",
    "combined score", "mean(score)",
    "min(IPDRatio)", "mean(IPDRatio)",
    "combined idQV", "mean(idQV)",
    "mean(coverage)"
]


def match_methylation_states_m6A(pos_plus, ipd_meth_states):
    state = set()
    pos_min = pos_plus+1
    for j, s in ((pos_plus, "+"), (pos_min, "-")):
        try:
            ipd_state = ipd_meth_states[j]
        except KeyError:
            pass
        else:
            if s == ipd_state:
                state.add(ipd_state)
    # logging.debug(
    #     f"[methylation report] {mol_id}: state {state} (pos={pos_plus})")
    if state == set():
        return "0"
    elif state < set("+-"):
        return state.pop()
    elif state == set("+-"):
        return "f"
    else:
        logging.error(
            f"[methylation report] inconsistent state {state} (pos={pos_plus})"
        )


# Improvement idea: add an __iter__ method to generate the lines of the
# methylation report.
# Refactor: move to own module
# Refactor: wraps reading/writing csv files completely (add static method
#           from file?)
class MethylationReport:
    _VALID_MODIFICATION_TYPES = ("m6A",)
    PRELOG = "[methylation report]"

    def __init__(
            self, detections_csv, molecules, modification_types,
            filtered_bam_statistics=None):
        self._detections_csv = Path(detections_csv)
        self._molecules = molecules
        base = self._detections_csv.name
        new_base = "methylation." + base
        self.csv_name = self._detections_csv.parent/new_base
        self.modification_types = modification_types
        self.filtered_bam_statistics = filtered_bam_statistics

    @property
    def modification_types(self):
        return self._modification_types

    @modification_types.setter
    def modification_types(self, values):
        self._modification_types = []
        for mod in values:
            if mod in self._VALID_MODIFICATION_TYPES:
                self._modification_types.append(mod)
            else:
                logging.warning(
                    f"{self.PRELOG} modifications of type '{mod}' will"
                    " be ignored"
                )

    def save(self):
        with open(self._detections_csv) as csv_in:
            csvreader = csv.reader(csv_in, delimiter=",")
            with open(self.csv_name, "w") as csv_out:
                csvwriter = csv.writer(csv_out, delimiter=";")
                csvwriter.writerow(METHYLATION_REPORT_HEADER)
                self._write_molecules(csvreader, csvwriter)

    def _write_molecules(self, csvreader, csvwriter):
        """This method implements the methylation report format V3
        It works only for m6A modification types.
        """

        # Idea to refactor this method: MoleculeSerializer

        mols_with_detections = {
            mol_id: list(detections) for mol_id, detections in
            groupby(csvreader, key=lambda x: x[0])
        }
        mols_with_detections = defaultdict(list, mols_with_detections)

        for mol_id in sorted(self._molecules):
            mol = self._molecules[mol_id]
            if mol.had_processing_problems:
                continue
            # The positions must be transformed to 1-base since
            # ipdSummary expects it:
            gatc_positions = [_.as_1base() for _ in mol.find_gatc_positions()]
            num_gatc = len(gatc_positions)

            ipd_meth_states = {}
            scores = []
            ipdratios = []
            idQVs = []
            coverages = []
            detections = mols_with_detections[str(mol_id)]
            if num_gatc > 0:
                for detection in detections:
                    modification = detection[1]
                    if modification in self.modification_types:
                        state = detection[4]
                        pos = int(detection[2])-1  # pos in the csv is 1-based
                        ipd_meth_states[pos] = state
                        scores.append(float(detection[3]))
                        ipdratios.append(float(detection[7]))
                        idQVs.append(float(detection[8]))
                        coverages.append(float(detection[5]))

            meth_states = {}
            for pos_plus in gatc_positions:
                out_state = match_methylation_states_m6A(
                    pos_plus, ipd_meth_states)
                if out_state:
                    meth_states[pos_plus] = out_state
            out_states = [meth_states[_] for _ in sorted(meth_states.keys())]

            # The next block is ugly. Must do something here...
            if self.filtered_bam_statistics is None:
                subreads = Counter()
            else:
                subreads = self.filtered_bam_statistics["subreads"].get(
                    mol_id, Counter())

            quals = [ord(_)-33 for _ in mol.ascii_quals]
            comb_qual = "{:0.1f}".format(combine_scores(quals))
            mean_qual = "{:0.1f}".format(mean(quals))

            sim_ratio = "{:g}".format(mol.cigar.sim_ratio)

            if num_gatc:
                num_meth_states = "{:d}".format(
                    len([_ for _ in out_states if _ != "0"]))
            else:
                num_meth_states = ""

            try:
                combined_scores = "{:0.1f}".format(combine_scores(scores))
            except ValueError:
                combined_scores = ""

            try:
                mean_scores = "{:0.1f}".format(mean(scores))
            except ValueError:
                mean_scores = ""

            try:
                min_ipdratio = "{:0.2f}".format(min(ipdratios))
            except ValueError:
                min_ipdratio = ""

            try:
                mean_ipdratio = "{:0.2f}".format(mean(ipdratios))
            except ValueError:
                mean_ipdratio = ""

            try:
                combined_idQVs = "{:0.1f}".format(combine_scores(idQVs))
            except ValueError:
                combined_idQVs = ""

            try:
                mean_idQVs = "{:0.1f}".format(mean(idQVs))
            except ValueError:
                mean_idQVs = ""

            try:
                mean_coverages = "{:0.0f}".format(mean(coverages))
            except ValueError:
                mean_coverages = ""

            # dna_pos is 0-based (Python convention), but the output must be
            # 1-based! since the gatc_positions are the 1-based positions of
            # the G, the positions output to the methylation report are
            # correct:
            row = (
                str(mol_id), mol.dna, str(mol.start.as_1base()), str(mol.end),
                str(len(mol)), str(subreads["+"]), str(subreads["-"]),
                comb_qual, mean_qual, sim_ratio, str(num_gatc),
                ",".join([str(_) for _ in gatc_positions]),
                num_meth_states, ",".join(out_states), combined_scores,
                mean_scores, min_ipdratio, mean_ipdratio, combined_idQVs,
                mean_idQVs, mean_coverages
            )
            csvwriter.writerow(row)
