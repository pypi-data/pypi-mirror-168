.. _quickstart:

============================
Quickstart for the impatient
============================

If you know how to install python packages from `PyPI`_ and how to
use the command line, you can follow the instructions in this
section to get |project| up and running.

Alternatively, if you need a step-by-step guide to use |project| on a cluster,
follow the :ref:`quickstart9steps` guide.

Installation
============

To install **PacBio Data Processing**, open an interactive shell and run:

.. prompt:: bash

  pip install PacBioDataProcessing

or, alternatively:

.. prompt:: bash

  python -m pip install PacBioDataProcessing


And that's it!

.. admonition:: On ``sm-analysis-gui``

   By default ``pip install PacBioDataProcessing`` does not enable the GUI
   program ``sm-analysis-gui``. This program is considered an extra feature,
   since its usage depends on the `wxpython`_ library, whose installation must be
   done independently.


.. note::

   More details as well as alternative installation methods are explained
   in :ref:`installation`.


.. warning::

   Although the installation of |project| is now complete, there are some
   *runtime* dependencies, which means that the dependencies *must be there*
   before *using* |project|. See :ref:`other-dependencies` and the links therein
   for the list of dependencies and suggestions on how to install them.


Using |project|
===============

Once |project| and its dependencies have been installed, the ``sm-analysis``
executable can be used to perform a single molecule analysis of ``m6A``
methylations in DNA. For that you need:

* a BAM file with the results of the sequencing, and
* the reference file: a ``.fa/.fasta`` (the companion
  ``.fa.fai/.fasta.fai`` file will be generated if missing)

and feed the ``sm-analysis`` program with those files.

For example, if the bam file's name is ``mysequence.bam`` and the reference
file is called ``myreference.fasta``, then the ``sm-analysis`` program will
carry out a single molecule analysis of the ``m6A`` methylations found
during sequencing with the following command:

  .. prompt:: bash

     sm-analysis mysequence.bam myreference.fasta


What's next?
============

In the :ref:`sm-analysis` section of the documentation you can find detailed
information about the output that you can expect from ``sm-analysis`` and
the possible input options available to customize its behaviour.

Check the :ref:`usage` section to learn more about how to use |project|.
Or have a look at the :ref:`guides` section for more advanced/specific
documentation on selected topics.

.. _wxpython: https://wxpython.org/
.. _PyPI: https://pypi.org/
