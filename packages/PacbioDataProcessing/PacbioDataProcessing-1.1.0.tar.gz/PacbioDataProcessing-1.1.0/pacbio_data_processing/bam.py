#######################################################################
#
# Copyright (C) 2021, 2022 David Palao
#
# This file is part of PacBio data processing.
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

import subprocess
from functools import cached_property, cache
from collections import namedtuple
import logging
from hashlib import md5
from pathlib import Path
import warnings
from typing import Protocol

import pysam

from pacbio_data_processing.constants import (
    SAMTOOLS_GET_HEADER, SAMTOOLS_GET_BODY, SAMTOOLS_WRITE_BAM,
)

MOLECULE_MARKER = b"zm:i:"
BAM_POS_COLUMN = 3
BAM_FLAG_COLUMN = 1
MAX_LINES_TO_CHECK_IN_BAM = 1000

_BAMFILEPYSAM_STRATEGY_CANONICAL = "_BamFilePysam"
_BAMFILEPYSAM_STRATEGY_ALIASES = (
    _BAMFILEPYSAM_STRATEGY_CANONICAL, "pysam"
)

_BAMFILESAMTOOLS_STRATEGY_CANONICAL = "_BamFileSamtools"
_BAMFILESAMTOOLS_STRATEGY_ALIASES = (
    _BAMFILESAMTOOLS_STRATEGY_CANONICAL, "samtools"
)

_DEFAULT_BAMFILE_STRATEGY = _BAMFILEPYSAM_STRATEGY_CANONICAL


class BamFileStrategy(Protocol):
    def __init__(self, bamfilename):
        ...

    def _read_header(self):
        ...

    def _read_body(self):
        ...

    def _write(self, *, header, body):
        ...


def pack_lines(lines):
    for line in lines:
        yield b"\t".join(line)+b"\n"


def set_pysam_verbosity():
    """Ad-hoc function to remove unpleasant errors messages by pysam."""
    api_error_common_msg = (
        "You might see some non-critical error messages from pysam."
    )
    try:
        pysam.set_verbosity(0)
    except AttributeError as e:
        logging.error(f"{e}. {api_error_common_msg}")
    except TypeError as e:
        logging.error(
            "'pysam.set_verbosity' failed. It looks like pysam changed its"
            " API. Continuing without setting the verbosity. "
            f"{api_error_common_msg}"
        )
    except Exception as e:
        logging.error(
            f"Unexpected error calling 'pysam.set_verbosity':\n{e}\n"
            f"Continuing without setting the verbosity. {api_error_common_msg}"
        )


def _strategy_factory(
        name: str = _DEFAULT_BAMFILE_STRATEGY) -> BamFileStrategy:
    """Internal function that returns the *strategy* class in a concrete
    ``BamFile`` instance.

    :meta public:
    """
    strategy = _BamFilePysam
    if name in _BAMFILEPYSAM_STRATEGY_ALIASES:
        pass
    elif name in _BAMFILESAMTOOLS_STRATEGY_ALIASES:
        strategy = _BamFileSamtools
    else:
        msg = (
            f"Unknown strategy name ({name}); using default strategy "
            f"({_DEFAULT_BAMFILE_STRATEGY})"
        )
        warnings.warn(msg)
    return strategy


@cache
def _BamLine_factory(*, num_columns: int, molecule_column: int) -> namedtuple:
    """Internal factory function that creates a custom BamLine class.
    It is used by ``_ReadBamFile`` to return a meaningful object for
    each line read.

    It is cached for obvious reasons: we want to avoid creation of
    the same class multiple times (every line!).
    """
    line_attrs = [f"attr{_}" for _ in range(num_columns)]
    line_attrs[molecule_column] = "zmw"

    class BamLine(namedtuple("BamLine", line_attrs)):
        @property
        def molecule_id(instance):
            return instance.zmw[len(MOLECULE_MARKER):]

        @property
        def flag(instance) -> int:
            return int(instance[BAM_FLAG_COLUMN])
    return BamLine


class BamFile:
    """Proxy class for ``_BamFileSamtools`` and ``_BamFilePysam``. This is
    a high level class whose only role is to choose among different
    possible *states*: ``_ReadableBamFile``  and ``_WritableBamFile``
    and to select the underlying implementation (*strategy*) to
    interact with the BAM file:

    - ``_BamFileSamtools``: implementation that simply wraps the
     'samtools' command line, and
    - ``_BamFilePysam``: implementation that uses 'pysam'

    The code is ready to permit the choice of strategy. With the current
    implementation it is, intentionally, a bit convoluted. For instance,
    instead of the default implementation (``pysam``), another one can
    be chosen as follows::

       from pacbio_data_processing.bam import BamFile
       BamFile.bamfile_strategy_name = "samtools"
       bam = BamFile("my.bam")

    and ``samtools`` will be used under the hood to get access to the data
    in a BAM file.
    """
    bamfile_strategy_name = _DEFAULT_BAMFILE_STRATEGY

    def __init__(self, bam_file_name, mode="r"):
        if mode == "r":
            self.__class__ = _ReadableBamFile
        elif mode == "w":
            self.__class__ = _WritableBamFile
        else:
            raise ValueError(f"invalid mode: '{mode}'")
        self._bamfile_strategy = _strategy_factory(self.bamfile_strategy_name)
        self._real_subject = self._bamfile_strategy(bam_file_name)

    def __getattr__(self, attr):
        return getattr(self._real_subject, attr)


class _ReadableBamFile(BamFile):
    """This class provides the attributes necessary for BamFile to be
    readable. Most attributes, e.g.

    - header
    - _BamLine
    - molecule_column
    - num_columns

    are cached, to avoid unnecessary IO ops (in the case of being a
    _BamFileSamtools object, an IO op would imply calling "samtools" each
    time the given attribute is read, which makes no sense since that would
    mean that the file has been modified after being opened, i.e. it has been
    most probably corrupted).

    The 'body' property is not cached as it is a generator of lines and it
    might make sense to read several times the same file.
    :meta public:
    """

    @cached_property
    def header(self):
        return self._read_header()

    @property
    def _BamLine(self):
        return _BamLine_factory(
            num_columns=self.num_columns,
            molecule_column=self.molecule_column
        )

    @property
    def body(self):
        for line in self._read_body():
            try:
                bamline = self._BamLine(*line)
            except TypeError:
                self.num_columns = len(line)
                bamline = self._BamLine(*line)
            yield bamline

    def __iter__(self):
        return self.body

    @cached_property
    def num_items(self) -> int:
        mols = set()
        for i, line in enumerate(self):
            mols.add(line.molecule_id)
        return {"molecules": len(mols), "subreads": i+1}

    @cached_property
    def molecule_column(self) -> int:
        line = next(self._read_body())
        for i, item in enumerate(line):
            if item.startswith(MOLECULE_MARKER):
                return i

    @cached_property
    def num_columns(self) -> int:
        """This property is tricky: the lines in a BAM file can have
        different number of columns within the same BAM file. The
        ``body`` generator will adjust the ``num_columns`` attribute
        as necessary.
        """
        line = next(self._read_body())
        return len(line)

    @property
    def num_molecules(self) -> int:
        return self.num_items["molecules"]

    @property
    def num_subreads(self) -> int:
        return self.num_items["subreads"]

    def __len__(self) -> int:
        return self.num_items["subreads"]

    @property
    def all_molecules(self):
        last = None
        for i, line in enumerate(self):
            mol_id = line.molecule_id
            if mol_id != last:
                yield mol_id
                last = mol_id

    @cached_property
    def is_aligned(self) -> bool:
        at_most = MAX_LINES_TO_CHECK_IN_BAM
        for iline, line in enumerate(self):
            if line[BAM_POS_COLUMN] == b"0":
                return False
            if iline > at_most:
                # exit early here assuming all the rest will be ok:
                break
        return True

    def is_plausible_aligned_version_of(self, other: BamFile) -> bool:
        """The main purpose of this *ad-hoc method* is to help
        SingleMoleculeAnalysis by providing a plausible answer to
        the question: *Does this BamFile look like an aligned version*
        *of another BamFile?*

        The implementation checks that the subject is aligned, the other
        is not and that the subject's set of molecules is a (proper)
        subset of the molecules in the other BamFile.

        Exceptions are propagated.
        """
        if self.is_aligned and (not other.is_aligned):
            mols = set(self.all_molecules)
            other_mols = set(other.all_molecules)
            if mols <= other_mols:
                return True
        return False

    @property
    def last_subreads_map(self) -> dict[bytes, int]:
        """It returns a mapping that answers the question: what is the
        index of the last subread corresponding to a certain molecule id?

        .. admonition:: Implementation detail

          This is *manually cached* because I was experiencing weird
          problems with ``cached_property`` that might have to do with
          https://github.com/python/cpython/issues/86293
          Anyway, I chose a poor man's solution that simply works.
        """
        try:
            subreads_map = self._subreads_map
        except AttributeError:
            subreads_map = {}
            for idx, subread in enumerate(self):
                subreads_map[subread.molecule_id] = idx
            self._subreads_map = subreads_map
        return subreads_map

    @cached_property
    def md5sum_body(self) -> str:
        """MD5 checksum of only the body of the BAM file, excluding the
        header"""
        checksum = md5()
        for line in pack_lines(self._read_body()):
            checksum.update(line)
        return checksum.hexdigest()

    @cached_property
    def full_md5sum(self) -> str:
        """MD5 checksum of the full file."""
        return md5(open(self.bam_file_name, "rb").read()).hexdigest()

    # It would be good to have something like:
    # def __getitem__(self, mol_id):
    #     for line in self:
    #         if line.molecule_id == mol_id:
    #             yield line

    @property
    def size_in_bytes(self) -> int:
        return Path(self.bam_file_name).stat().st_size


class _WritableBamFile(BamFile):
    def write(self, *, header, body):
        self._write(header=header, body=body)


class _BamFileSamtools:
    """Strategy implementation that wraps the 'samtools' executable.
    :meta public:
    """
    def __init__(self, bam_file_name):
        # A refactor of __init__ would probably need an ABC...
        self.bam_file_name = bam_file_name

    def _read_header(self):
        # check for errors and report them if any. Need FT!
        return subprocess.run(
            SAMTOOLS_GET_HEADER+(self.bam_file_name,), capture_output=True
        ).stdout

    def _read_body(self):
        with subprocess.Popen(
                SAMTOOLS_GET_BODY+(self.bam_file_name,), stdout=subprocess.PIPE
                ) as body:
            for line in body.stdout:
                yield line.split()

    def _write(self, *, header, body):
        with open(self.bam_file_name, "wb") as bam_file:
            with subprocess.Popen(
                    SAMTOOLS_WRITE_BAM, stdin=subprocess.PIPE, stdout=bam_file
                    ) as proc:
                proc.stdin.write(header)
                for line in pack_lines(body):
                    proc.stdin.write(line)


class _BamFilePysam:
    """Strategy implementation that uses 'pysam'.
    :meta public:
    """
    _PYSAM_VERBOSITY_SET = False

    def __init__(self, bam_file_name):
        self.bam_file_name = bam_file_name
        self.set_pysam_verbosity_once()

    @classmethod
    def set_pysam_verbosity_once(cls):
        """This class method helps to ensure that set_pysam_verbosity
        is called only once, the first time an instance is created."""
        if cls._PYSAM_VERBOSITY_SET is False:
            set_pysam_verbosity()
            cls._PYSAM_VERBOSITY_SET = True

    @property
    def _ralignment_file(self):
        """An AlignmentFile instance is created for READING."""
        return pysam.AlignmentFile(self.bam_file_name, "rb", check_sq=False)

    def _read_header(self):
        return str(self._ralignment_file.header).encode()

    def _read_body(self):
        for line in self._ralignment_file:
            yield line.to_string().encode().split()

    def _write(self, *, header, body):
        # Need to be sure that there is a single "\n" at the end:
        h = pysam.AlignmentHeader.from_text(header.decode().rstrip()+"\n")
        with pysam.AlignmentFile(self.bam_file_name, "wb", header=h) as g:
            header = g.header
            for line in pack_lines(body):
                g.write(pysam.AlignedSegment.fromstring(
                    # Need to be sure that there is no "\n" between lines:
                    line.decode().strip(), header)
                )
