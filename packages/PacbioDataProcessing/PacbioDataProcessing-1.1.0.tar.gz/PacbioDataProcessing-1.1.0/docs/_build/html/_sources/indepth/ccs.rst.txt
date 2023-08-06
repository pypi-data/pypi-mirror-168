.. highlight:: shell

.. _about-ccs:

CCS
===

The :ref:`sm-analysis program <sm-analysis>` uses the ``ccs`` program to
obtain highly accurate reads from the input BAM that are taken as the
true sequences and positions within the reference for each molecule in
the analysis done by the :ref:`sm-analysis program <sm-analysis>`.

``ccs`` is a *runtime* dependency: it must be accessible at *latest* at
runtime and it is called on demand: if its output is already there, it will
not be computed again.

By default, ``ccs`` is searched for in the :term:`PATH`. If it is
not found in the :term:`PATH`, you will receive a common runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'ccs'

and the :ref:`sm-analysis program <sm-analysis>` itself will terminate.

In that case, the instructions in the following sections can help you.


Installing CCS
--------------

An easy way to install the ``ccs`` program is with ``conda``.
Have a look at :ref:`setting_up_bioconda`, and follow the instructions, if
you haOnce those steps are followed,
and the resulting ``conda`` environment is *active*, install ``pbccs``:

.. code-block:: console

   $ conda install pbccs

.. warning::

   Notice that, contrary to the suggestion given in `PacBio & Bioconda`_,
   the explicit selection of the ``bioconda`` channel by means of the ``-c``
   option of ``conda install`` (e.g., ``conda install -c bioconda ...``)
   triggers a dependency error. DO NOT USE the ``-c bioconda`` option,
   just run ``conda install ...`` instead, as explained in the main text.

.. note::

   An alternative way to install ``pbindex`` is through :ref:`SMRT LINK`.

Upon success, you will be able to pass the path to the ``ccs``
executable to :ref:`sm-analysis <sm-analysis>` if needed (see
below for details).


Using ccs from `sm-analysis`
------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/dave/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/dave/miniconda3

then, after activating the |project|'s virtual environment:

.. code-block:: console

   $ source /home/dave/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``ccs`` by using a command
line option (:option:`sm-analysis -c`) as follows:

.. code-block:: console

   $ sm-analysis --ccs-path /home/dave/miniconda3/bin/ccs


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels


Issues
------

Multimapping
^^^^^^^^^^^^

In some cases an aligned CCS file presents multimapping. Two examples take from the
``st1A09`` file::

  m54099_200720_153206/4194505/ccs        0       U00096.3        392180  0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        256     U00096.3        1094716 0       150=    *       0       0       ATCTGTACGTAAGTACGTGATGTCTCCTGCCCACTTCT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        2170808 0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        567414  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  m54099_200720_153206/4194505/ccs        272     U00096.3        315863  0       150=    *       0       0       GGACTGAGGGCAAAGGCCTCCCGGAAGTTCAGCCCGGT...
  ...
  m54099_200720_153206/4194627/ccs        0       U00096.3        274198  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        574834  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        688094  0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        3130803 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2101992 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        2289162 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1396701 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        272     U00096.3        1300156 0       295=    *       0       0       CGGCCAACGAGCATGACCTCAATCAGCTGGGTAATCTG...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3365799 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...
  m54099_200720_153206/4194627/ccs        256     U00096.3        3652279 0       295=    *       0       0       CCCTTGTATCTGGCTTTCACGAAGCCGAACTGTCGCTT...

How do we decide the position? In the current implementation, the first
subread of each molecule is taken (for details, see
:py:func:`pacbio_data_processing.sm_analysis.map_molecules_with_highest_sim_ratio`),
because all the subreads are *perfect*. But notice that the positions (4th
column) differ.
