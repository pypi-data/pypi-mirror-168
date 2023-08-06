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

import unittest
from unittest.mock import patch, MagicMock, call, mock_open
from pathlib import Path

from pacbio_data_processing.methylation import (
    MethylationReport, METHYLATION_REPORT_HEADER, match_methylation_states_m6A
)
from pacbio_data_processing.bam_utils import Molecule


class MethylationReportTestCase(unittest.TestCase):
    REFERENCE = (
        "CATTGATCCCGGCACCAGGCTGCACGACGTTAACGATGATAAGACCAATAATCAGCGCGATG"
        "GTACT"
        + "A"*50 +
        "AAGTTCGGGCAAATGTTATCAACCCGCCGCGATCTTTTTCCACCGCATATTGCCGATCAGCT"
        "GGCGTTATTGCAGGACAAAGTTGCTCCGTTTGATGGCAAGCTGGCGAAGCAGCAGATTGAAGC"
        "TGCAATGGGCGGCTTGCCGGTAGAAGCGTGGTTTGACGATTTTGAAATCAAGCCGCTGGCTTC"
        "TGCTTCTATCGCCCAGGTTCATACCGCGCGATTGAAATCGAATGGTAAAGAGGTGGTGATTAA"
        "AGTCATCCGCCCGGATATTTTGCCGGTTATTAAAGCGGATCTGAAACTTATCTACCGTCTGGC"
        "TCGCTGGGTGCCGCGTTT"
        + "C"*50 +
        "AAAGGATCTGTAATTAGTCGACCAGCGGATCGAATGTTATAATACGCGCCAATAAAAACGGC"
        "TCAGATCTTCATCTGCCA"
        + "G"*50 +
        "ATTGCATCTGTAATTAGTCGACCAGCGGATGGAATGTTATAATACGCGCCAATTGCAACGGC"
        "TCAACTCAGCTCCTGCCA"
        + "T"*50 +
        "CTGGTCTTTCGCCTGATCGGCGTAAACCGCTACCGCTTTCGCATCAAGCGTTGCCGGACGTT"
    )

    MOLECULE_LINES = {
        350: (
            b"m54099_200711_014004/350/ccs", b"16", b"U00096.3",
            b"118", b"254", b"332=", b"*", b"0", b"0",
            (b"AAGTTCGGGCAAATGTTATCAACCCGCCGCGATCTTTTTCCACCGCATATTGCCGATCAGCT"
             b"GGCGTTATTGCAGGACAAAGTTGCTCCGTTTGATGGCAAGCTGGCGAAGCAGCAGATTGAAGC"
             b"TGCAATGGGCGGCTTGCCGGTAGAAGCGTGGTTTGACGATTTTGAAATCAAGCCGCTGGCTTC"
             b"TGCTTCTATCGCCCAGGTTCATACCGCGCGATTGAAATCGAATGGTAAAGAGGTGGTGATTAA"
             b"AGTCATCCGCCCGGATATTTTGCCGGTTATTAAAGCGGATCTGAAACTTATCTACCGTCTGGC"
             b"TCGCTGGGTGCCGCGTTT"),
            b"~"*100+b"1234567890qwertyuiopasdfghjklzxcvbnm,.-<>;"+b"~"*200,
            b"RG:Z:3d1638a6", b"ec:f:60", b"np:i:60", b"rq:f:1",
            b"sn:B:f,5.47248,10.074,6.52768,11.3767", b"zm:i:350",
            b"AS:i:-1660", b"NM:i:0"
        ),
        401: (
            b"m54099_200711_014004/401/ccs", b"16", b"U00096.3",
            b"500", b"254", b"80=", b"*", b"0", b"0",
            (b"AAAGGATCTGTAATTAGTCGACCAGCGGATCGAATGTTATAATACGCGCCAATAAAAACGGC"
             b"TCAGATCTTCATCTGCCA"),
            b"~"*30+b"+"*10+b"'"*10+b"Q"*10+b"_"*10+b"="*10,
            b"RG:Z:3d1638a6", b"ec:f:60", b"np:i:60", b"rq:f:1",
            b"sn:B:f,5.47248,10.074,6.52768,11.3767", b"zm:i:401",
            b"AS:i:-1660", b"NM:i:0"
        ),
        405: (
            b"m54099_200711_014004/405/ccs", b"16", b"U00096.3",
            b"630", b"254", b"80=", b"*", b"0", b"0",
            (b"ATTGCATCTGTAATTAGTCGACCAGCGGATGGAATGTTATAATACGCGCCAATTGCAACGGC"
             b"TCAACTCAGCTCCTGCCA"),
            b"~"*80,
            b"RG:Z:3d1638a6", b"ec:f:60", b"np:i:60", b"rq:f:1",
            b"sn:B:f,5.47248,10.074,6.52768,11.3767", b"zm:i:405",
            b"AS:i:-1660", b"NM:i:0"
        ),
        456: (
            b"m54099_200711_014004/456/ccs", b"16", b"U00096.3",
            b"760", b"254", b"129=", b"*", b"0", b"0",
            (b"CTGGTCTTTCGCCTGATCGGCGTAAACCGCTACCGCTTTCGCATCAAGCGTTGCCGGACGTT"
             b"CATTGATCCCGGCACCAGGCTGCACGACGTTAACGATGATAAGACCAATAATCAGCGCGATG"
             b"GTACT"),
            b"~"*100+b"}"*29,
            b"RG:Z:3d1638a6", b"ec:f:60", b"np:i:60", b"rq:f:1",
            b"sn:B:f,5.30539,9.67227,6.35734,11.0005", b"zm:i:456",
            b"AS:i:-645", b"NM:i:0"
        ),
    }
    IPD_METHYLATIONS = [
        ("401", "m6A", "506", "52", "-", "25",
         "TGAAGCTGATCAGAAGGGTGATCCGAAGTGGGATCTACGAG", "5.31", "34"),
        ("401", "m6A", "528", "61", "+", "24",
         "CACTTCGGATCACCCTTCTGATCAGCTTCACTACCTTCCAC", "7.16", "39"),
        ("401", "m6A", "529", "41", "-", "25",
         "TGTGGAAGGTAGTGAAGCTGATCAGAAGGGTGATCCGAAGT", "6.68", "13"),
        ("405", "m4C", "636", "23", "+", "99",
         "GCAGCTACGGTTTCGATTTCCTCCACCGGCGCATTTTCCAG", "1.42", "11"),
        ("405", "m6A", "640", "41", "-", "25",
         "TGTGGAAGGTAGTGAAGCTGATAAGAAGGGTGCTCCGAAGT", "2.68", "8"),
        ("456", "m6A", "775", "25", "+", "9",
         "CTATGCTTTGCGCTGCCACGATCGCGACATAGATCCCACAT", "6.81", "10"),
        ("456", "m6A", "6", "27", "+", "7",
         "CTGCCACGATCGCGACATAGATCCCACATCGGATCGCGCAA", "6.82", "5"),
        ("456", "m4C", "818", "47", "-", "17",
         "CTGCCACGATCGCGACATAGATCCCACATCGGATCGCGCAA", "16.82", "52"),
        ("461", "m6A", "192", "22", "-", "15",
         "TGATCGTTGCCGCGCATAGCAATGCCCGGCAGGACAGAGCA", "2.45", "3"),
        ("461", "m6A", "191", "24", "+", "15",
         "CATTGCTATGCGCGGCAACGATCACGTCCTAGATCCCGCAT", "3.51", "3"),
        ("461", "m6A", "196", "23", "-", "15",
         "GATGCGGGATCTAGGACGTGATCGTTGCCGCGCATAGCAAT", "3.20", "4"),
        ("461", "m6A", "195", "25", "+", "15",
         "CGGCAACGATCACGTCCTAGATCCCGCATCGGATCACGCTT", "4.10", "4"),
        ("461", "m4C", "204", "72", "-", "88",
         "TGATCGTTGCCGCGCATAGCAATGCCCGGCAGGACAGAGCA", "12.45", "33"),
        ("507", "m6A", "440", "110", "+", "128",
         "GGTTAGGCACCAGGCTGCACGATCGATAAGACCAATAATCA", "19.33", "58"),
        ("507", "m6A", "441", "109", "-", "132",
         "GGTTAGGCACCAGGCTGCACGATCGATAAGACCAATAATCA", "17.46", "47"),
    ]
    METHYLATIONS_PER_MOLECULE = [
        (
            "350",
            ("AAGTTCGGGCAAATGTTATCAACCCGCCGCGATCTTTTTCCACCGCATATTGCCGATCAGCT"
             "GGCGTTATTGCAGGACAAAGTTGCTCCGTTTGATGGCAAGCTGGCGAAGCAGCAGATTGAAGC"
             "TGCAATGGGCGGCTTGCCGGTAGAAGCGTGGTTTGACGATTTTGAAATCAAGCCGCTGGCTTC"
             "TGCTTCTATCGCCCAGGTTCATACCGCGCGATTGAAATCGAATGGTAAAGAGGTGGTGATTAA"
             "AGTCATCCGCCCGGATATTTTGCCGGTTATTAAAGCGGATCTGAAACTTATCTACCGTCTGGC"
             "TCGCTGGGTGCCGCGTTT"),
            "118", "449", "332", "25", "27", "5.4", "88.3", "1", "3",
            "148,172,406", "0", "0,0,0", "", "", "", "", "", "", ""
        ),
        (
            "401",
            ("AAAGGATCTGTAATTAGTCGACCAGCGGATCGAATGTTATAATACGCGCCAATAAAAA"
             "CGGCTCAGATCTTCATCTGCCA"), "500", "579",
            "80", "120", "120", "0.1", "54.1", "1", "3",
            "504,527,565", "2", "-,f,0", "40.6", "51.3", "5.31", "6.38",
            "13.0", "28.7", "25"
        ),
        (
            "405",
            ("ATTGCATCTGTAATTAGTCGACCAGCGGATGGAATGTTATAATACGCGCCAATTGCAACGGC"
             "TCAACTCAGCTCCTGCCA"),
            "630", "709", "80", "89", "88", "74.0", "93.0",
            "1", "0", "", "", "", "", "", "", "", "", "", ""
        ),
        (
            "456",
            ("CTGGTCTTTCGCCTGATCGGCGTAAACCGCTACCGCTTTCGCATCAAGCGTTGCCGGACG"
             "TTCATTGATCCCGGCACCAGGCTGCACGACGTTAACGATGATAAGACCAATAATCAGCGCG"
             "ATGGTACT"),
            "760", "67", "129", "50", "149", "71.6", "92.8",
            "1", "2", "774,5", "2", "+,+", "22.9", "26.0", "6.81", "6.81",
            "4.1", "7.5", "8"

        ),
    ]

    SUBREADS_PER_MOLECULE = {
        350: {"+": 25, "-": 27},
        401: {"+": 120, "-": 120},
        405: {"+": 89, "-": 88},
        456: {"+": 50, "-": 149},
    }

    @classmethod
    def setUpClass(cls):
        """Tasks performed in this method:
        1) Prepare a reference sequence"""
        cls.MOLECULES = {}
        for idx, l in cls.MOLECULE_LINES.items():
            mol = Molecule(idx, "", l)
            mol.reference = cls.REFERENCE
            mol.had_processing_problems = False
            cls.MOLECULES[idx] = mol

        # What is all the rest doing!?
        # mols = [
        #     (idx, cls.MOLECULES[idx]) for idx in
        #     ("456", "350", "401", "405")
        # ]
        # seqs = []
        # prev = 0
        # for idx, mol in mols:
        #     current = int(mol[3].decode())-1
        #     if idx == "507":
        #         seq = mol[9].decode()
        #         seq = seq[:10]+seq[11:]
        #     else:
        #         seq = mol[9].decode()
        #     seqs.append("?"*(current-prev))
        #     seqs.append(seq)
        #     prev = current+len(seq)

    def test_sets_some_attributes(self):
        mr = MethylationReport(
            detections_csv="a/b/c.csv",
            molecules={2: None},
            modification_types=["m6A"],
        )
        self.assertEqual(str(mr.csv_name), "a/b/methylation.c.csv")
        self.assertIs(mr.filtered_bam_statistics, None)
        self.assertEqual(mr._molecules, {2: None})

    def test_modification_types_get_validated(self):
        mr = MethylationReport(
            detections_csv="some.csv", molecules={},
            modification_types=["m6A"]
        )
        self.assertEqual(mr.modification_types, ["m6A"])
        mr = MethylationReport(
            detections_csv="some.csv", molecules={},
            modification_types=["?"]
        )
        self.assertEqual(mr.modification_types, [])
        mr = MethylationReport(
            detections_csv="some.csv", molecules={},
            modification_types=["?", "m6A"]
        )
        self.assertEqual(mr.modification_types, ["m6A"])

    def test_emits_log_message_for_each_invalid_modification_type(self):
        with self.assertLogs() as cm:
            MethylationReport(
                detections_csv="some.csv", molecules={},
                modification_types=["?", "m6A", "m4C"]
            )
        template = (
            "[methylation report] modifications of type '{mod}' will be "
            "ignored"
        )
        self.assertEqual(
            cm.output,
            ["WARNING:root:"+template.format(mod="?"),
             "WARNING:root:"+template.format(mod="m4C")]
        )

    @patch("pacbio_data_processing.methylation.csv.reader")
    @patch("pacbio_data_processing.methylation.csv.writer")
    @patch("pacbio_data_processing.methylation.MethylationReport."
           "_write_molecules")
    @patch("pacbio_data_processing.methylation.open")
    def test_save_writes_header_and_calls_write_molecules(
            self, mopen, pwrite_molecules, pwriter, preader):
        mopen_write = mock_open()
        mopen_read = mock_open(read_data="")
        mopen.side_effect = [mopen_read.return_value, mopen_write.return_value]
        mr = MethylationReport(
            detections_csv="a/b/c.csv", molecules={},
            modification_types=["m6A"],
        )
        mr.save()
        mopen.assert_has_calls(
            [call(Path("a/b/c.csv")), call(mr.csv_name, "w")])
        preader.assert_called_once_with(
            mopen_read().__enter__(), delimiter=',')
        pwriter.assert_called_once_with(
            mopen_write().__enter__(), delimiter=';')
        pwriter.return_value.writerow.assert_called_once_with(
            METHYLATION_REPORT_HEADER)
        pwrite_molecules.assert_called_once_with(
            preader.return_value, pwriter.return_value)

    def test_write_molecules_writes_one_line_per_expected_molecule(self):
        reader = MagicMock()
        writer = MagicMock()
        reader.__iter__ = MagicMock(return_value=iter(self.IPD_METHYLATIONS))
        mr = MethylationReport(
            detections_csv="a/b/c.csv", molecules=self.MOLECULES,
            modification_types=["m6A"]
        )
        mr.filtered_bam_statistics = {"subreads": self.SUBREADS_PER_MOLECULE}
        mr._write_molecules(reader, writer)
        writer.writerow.assert_has_calls(
            [call(_) for _ in self.METHYLATIONS_PER_MOLECULE]
        )
        self.assertEqual(
            len(writer.writerow.mock_calls),
            len(self.METHYLATIONS_PER_MOLECULE)
        )

    def test_write_molecules_doesnt_write_molecules_without_methylations(self):
        reader = MagicMock()
        writer = MagicMock()
        reader.__iter__ = MagicMock(return_value=iter(self.IPD_METHYLATIONS))
        mr = MethylationReport(
            detections_csv="a/b/c.csv", molecules=self.MOLECULES,
            modification_types=["m6A"]
        )
        mr._write_molecules(reader, writer)
        for c in writer.writerow.mock_calls:
            self.assertNotEqual(c[1][0][0], "461")

    def test_write_molecules_doesnt_write_molecules_with_problems(self):
        reader = MagicMock()
        writer = MagicMock()
        reader.__iter__ = MagicMock(return_value=iter(self.IPD_METHYLATIONS))
        self.MOLECULES[350].had_processing_problems = True
        mr = MethylationReport(
            detections_csv="a/b/c.csv", molecules=self.MOLECULES,
            modification_types=["m6A"]
        )
        mr._write_molecules(reader, writer)
        for c in writer.writerow.mock_calls:
            self.assertNotEqual(c[1][0][0], "350")
        self.MOLECULES[350].had_processing_problems = False


class MatchMethylationStatesTestCase(unittest.TestCase):
    def test_returns_zero_if_no_matching_state(self):
        for ipd_meth_states in ({}, {5: "-"}):
            self.assertEqual(
                match_methylation_states_m6A(5, ipd_meth_states), "0")

    def test_returns_plus_or_minus_if_one_match(self):
        in_ipd_meth_states = [
            {24: "-"},
            {14: "+"},
            {82: "+", 84: "-"}
        ]
        expected_results = ["-", "+", "-"]
        plus_positions = [23, 14, 83]
        for i, ipd_meth_states in enumerate(in_ipd_meth_states):
            pos = plus_positions[i]
            expected = expected_results[i]
            with self.subTest(pos=pos):
                self.assertEqual(
                    match_methylation_states_m6A(pos, ipd_meth_states),
                    expected
                )

    def test_returns_f_if_two_matches(self):
        in_ipd_meth_states = [
            {24: "-", 23: "+"},
            {14: "+", 15: "-"},
            {83: "+", 84: "-", 87: "+"}
        ]
        plus_positions = [23, 14, 83]
        for i, ipd_meth_states in enumerate(in_ipd_meth_states):
            pos = plus_positions[i]
            with self.subTest(pos=pos):
                self.assertEqual(
                    match_methylation_states_m6A(pos, ipd_meth_states), "f"
                )
