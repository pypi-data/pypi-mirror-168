.. _summary-report:

===============
Summary Reports
===============

.. sectionauthor:: David Palao <david.palao@gmail.com>

.. only:: internal

   :Author: David Palao
   :Date: 22 June 2022
   :Last updated: 28 June 2022
   :Tags: sm-analysis PacbioDataProcessing output summary-report
       
:abstract:

   The :ref:`sm-analysis <sm-analysis>` program summarizes some
   statistics about the analysis with a file aptly called
   *summary report*. This document describes its contents.


Introduction
============

Most of the data found in the :term:`summary report` are self-explanatory,
but some points deserve special attention. The aim of this document is to
provide additional comments that help to understand the precise meaning
and/or format of the quantities reported in the sumamry report.


Description
===========

The remaining subsections of this document map the sections of the
summary report. Not every quantity that appears in a summary report is
described below, though. Only the points that require additional
remarks are documented here.


Overview
--------

This section contains general information about the particular run of
:ref:`sm-analysis` that produced the summary report in question. The
command given to produce the analysis can be obtained by joining
**Program name** to **Program options**. The date of the analysis
contains the date *and* time when the :ref:`sm-analysis <sm-analysis>`
program started, and is given in the ISO 8601 format with a precision
of minutes, following this pattern: ``YYYY-MM-DDTHH:MM``.


Result filenames
----------------

The :ref:`sm-analysis` program produces different output files. Local
links to those files are provided in this section. See 
:ref:`methylation-report-format`, :ref:`raw-detections-format` and
`GFF format`_ for a description of their contents. Notice that actually
the link to the **GFF** file is pointing to a *concatenation* of all
GFF files produced by :ref:`ipdSummary <kineticsTools>`.


Input files
-----------

This section contains details about the input files passed in to
the :ref:`sm-analysis`: the BAM file and the :term:`reference` file.

     
BAM File
^^^^^^^^

Apart from the filename and the size in bytes, the report includes
the :term:`MD5 checksum` of the *full* file, as it was at the time of the
analysis, and the :term:`MD5 checksum` of the *body* of that file. The
reason for adding both is that the header of the BAM file could be altered
by some tool while the body is preserved intact. In a normal case, the
full checksum would be enough. But if, by some reason, the header of the BAM
file was modified after the analysis, having the body checksum at hand
could be helpful.


Reference
^^^^^^^^^

Apart from the filename, a :term:`FASTA` file contains a reference
*name*, which is given under *Reference name*. The length of the sequence
itself is also given (in terms of base pairs) and the :term:`MD5 checksum`
of the (normalized to upper case) sequence is included as well.


Molecules/subreads
------------------

Basic statistics about the body of the input BAM file. All the quantities
in this section are given for :term:`molecules <molecule>` and for
:term:`subreads <subread>`.

**Initial** contains the molecules/subreads counts in the input BAM file.
All percentages in this section refer to these quantities. In particular,
the statistics about :term:`subreads <subread>` refer to what is found in
the input BAM file.

**Used in aligned CCS BAM** refers to how many molecules/subreads from the
input BAM file are *also* in *any* of the
:term:`alignment variants <alignment variant>` of the CCS BAM file.
Each molecule from the input BAM file will be assigned, *at most*, to one
:term:`variant`, i.e. even if a molecule is found in all the alignment
variants, it (and its subreads) will not be counted more than once. 


**DNA mismatch discards** gives us the numbers corresponding to molecules
for which the sequence provided by the aligned CCS BAM file
*does not match* the reference at the position given also by the aligned
CCS BAM file.

**Filtered out** contains statistics about the molecules discarded by the
filters applied by :ref:`sm-analysis` to the input BAM file.

**Faulty (with processing error)** are :term:`molecules <molecule>` whose
corresponding single molecule BAM file had problems when it was processed by
either :ref:`pbindex <about-pbindex>` or :ref:`ipdSummary <kineticsTools>`.
The details about what went wrong are given in the output displayed in the
screen *if* the :ref:`sm-analysis <sm-analysis>` program was executed in
*verbose mode*, i.e. :option:`sm-analysis -v`. Faulty molecules
are exceptional. A normal :ref:`sm-analysis` is expected to have not even
a single faulty molecule.

The **In methylation report...** row contains what fraction of the initial
data ends up in the :ref:`methylation report <methylation-report-format>`.
These quantities are further splitted into which :term:`molecules <molecule>`
and :term:`subreads <subread>` contain/do not contain GATCs in the rows
**...only with GATCs** and **...only without GATCs**, respectively.
Of course, **...only with GATCs** and **...only without GATCs** add up to
**In methylation report...**.

The quantities in **Used in aligned CCS BAM** should be the sum of the
corresponding numbers found in the following rows: **DNA mismatch discards**,
**Filtered out**, **Faulty (with processing error)** and
**In methylation report...**. The difference between **Initial** and
**Used in aligned CCS BAM** is due to :term:`molecules <molecule>` that
do not *survive* the CCS and alignment processes. Since the positioning
of the molecules is essential to determine the location of the detected
methylation, the aligned CCS BAM file is taken as a baseline.

.. versionadded:: 1.0

   **Faulty (with processing error)** added to the summary report.


Sequencing Position Coverage
----------------------------

**Positions covered by molecules in the BAM file** refer to the position
coverage provided by all the :term:`molecules <molecule>` in all the
:term:`alignment variants <alignment variant>` of the CCS BAM file.
Obviously the percentages in this section refer to the length of the
:term:`reference`.


GATCs
-----

Again, as in the section **Sequencing Position Coverage**, the 
**Number of GATCs identified in the BAM file** include all the
:term:`molecules <molecule>` in the merged
:term:`alignment variants <alignment variant>` of the CCS BAM file.


Methylations
------------

As the summary report itself declares, in this section the *individual*
methylation detections are considered. Any GATC in the :term:`reference`
can be detected multiple times: several :term:`molecules <molecule>`
can cover the same GATC, but each molecule will be analyzed independently
by :ref:`sm-analysis <sm-analysis>`. That is why
**Total number of GATCs in all the analyzed molecules** does not
(and must not!) agree with the numbers in the **GATCs** section.

.. _`GFF format`: https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
