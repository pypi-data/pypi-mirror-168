.. _raw-detections-format:

==============
Raw Detections
==============

.. sectionauthor:: David Palao <david.palao@gmail.com>

.. only:: internal

   :Author: David Palao
   :Date: 28 June 2022
   :Last updated: 28 June 2022
   :Version: N/A
   :Tags: sm-analysis PacbioDataProcessing output detection
       
The :ref:`sm-analysis` pipeline produces a so-called
*raw detections report* also informally called *own output*.

The *raw detections* file contains, as the name suggests, *raw* data
coming directly from the :ref:`ipdSummary <kineticsTools>` program.
That data is used by :ref:`sm-analysis <sm-analysis>` to produce the
:ref:`methylation report <methylation-report-format>`, which is
a detailed view (*per molecule*) of the methylation status of individual
molecules for each GATC in that molecule.

The *raw detections* file is a :term:`CSV file`. Each line in this file
corresponds to an individual detection. Its format used by  described in
:py:func:`pacbio_data_processing.sm_analysis.add_to_own_output`
