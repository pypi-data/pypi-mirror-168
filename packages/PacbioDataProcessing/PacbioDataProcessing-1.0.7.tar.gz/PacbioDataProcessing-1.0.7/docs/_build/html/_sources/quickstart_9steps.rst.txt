.. _quickstart9steps:

=======================
Quickstart on a cluster
=======================

This is a very synthetic document that summarizes the steps necessary to install
and use the |project| software on a cluster. Not many details are given
here, since this document is only intended to be a brief reference. If you need
more details on each step, please follow the provided links.

Goal
====

Starting with a PacBio sequencing file (bam file) and a
reference sequence (fasta file), the `sm-analysis` tool from |project| will
generate a csv file (a so-called :ref:`methylation report <methylation-report-format>`).
Each row corresponds to one molecule, (*hole number* or *ZMW* in the PacBio parlance)
with columns containing properties for each molecule that overcame good
quality filters.

Additional to this, a :ref:`summary-report` is generated containing some basic
statistics about the input, the process and output files.

Steps
=====

1. Create a cluster account. Needless to say, this step is strongly dependent
   on the cluster and details cannot be given here (but see
   :ref:`using-a-cluster` if you plan to use the `Goethe-HLR cluster`_).

2. Open a terminal and login to access to the cluster
   (see :ref:`using-a-cluster`).

3. Install Python-3.9 (or above) in the cluster (see the :ref:`installation` document).

4. Create a virtual environment (see the :ref:`installation` document).

5. Install the external dependences :ref:`pbindex <about-pbindex>`,
   :ref:`pbmm2 <aligners>`, :ref:`kineticsTools` and :ref:`ccs <about-ccs>`
   (see the :ref:`using-a-cluster` document).

6. Install |project| (see the :ref:`installation` document).

7. Copy the input files to the cluster. Assuming that you want to process
   a file called ``pbsequencing.bam`` and your reference is stored in
   a file called ``reference.fasta`` (with its companion index
   ``reference.fasta.fai``), run the following command in a terminal:

   .. code-block:: console

       scp pbsequencing.bam reference.fasta{,.fai} dave@goethe.hhlr-gu.de:/scratch/fuchs/darmstadt/dave/myproject/

   YMMV: the paths will change depending on the name of your account,
   and the destination directory. The destination directory must exist.
   Recent versions of ``rsync`` accept a ``--mkpath`` option to create missing
   components of the destination path; don't count on having
   recent versions of software by default on a cluster ;-)

   .. note::

      The cluster administrators tend to be very concerned about a proper usage of the
      filesystems available in a cluster. Quite often they provide different filesystems
      with different properties (speed, size, etc) along with suggestions and policies to
      use them properly. Try to find out what is the situation in your case and stick, as
      much as you can, to their policy to minimize performance problems.
      On the `Goethe-HLR cluster`_ website you can learn about filesystems in the
      `Goethe-HLR storage`_ or `FUCHS-CSC storage`_ sections.

8. Prepare and submit a Job (see :ref:`using-a-cluster`). This step is where the
   analysis done by |project| is carried out.

9. Copy the output files to your personal computer:

   .. code-block:: console

       scp dave@goethe.hhlr-gu.de:/scratch/fuchs/darmstadt/dave/[file to transfer] .

   where the trailing ``.`` (*dot*) can be replaced by any other *local path*,
   of course. The special case of ``.`` means *current working directory*.

   Or, to synchronize the remote location with your current working directory:

   .. code-block:: console

       rsync -avz dave@goethe.hhlr-gu.de:/scratch/fuchs/darmstadt/dave/myproject/ ./


.. _Goethe-HLR cluster: https://csc.uni-frankfurt.de/
.. _Goethe-HLR storage: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:goethe#storage
.. _FUCHS-CSC storage: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:fuchs#storage
