.. highlight:: shell

.. _about-blasr:

Blasr
=====

The :ref:`sm-analysis program <sm-analysis>` delegates the alignment of the input BAM
file to ``blasr``, which must be accessible at runtime. The ``blasr``
program will be called on demand: if an aligned file is found,
the alignment process will be skipped for that file.

By default, ``blasr`` is searched for in the :term:`PATH`. If it is
not found in the :term:`PATH`, you will receive a common runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'blasr'

and the :ref:`sm-analysis program <sm-analysis>` itself will terminate.

In that case, the instructions in the following sections can help you.


Installing Blasr
----------------

Probably the easiest way to install ``blasr`` is with ``conda``.
Have a look at :ref:`setting_up_bioconda`. Once those steps are followed,
and the resulting ``conda`` environment is *active*, install ``blasr``:

.. code-block:: console
	    
   $ conda install blasr

Upon success, you will be able to pass the path to the ``blasr``
executable to :ref:`sm-analysis <sm-analysis>` if needed (see below for details).

.. warning::

   Notice that, contrary to the suggestion given in `PacBio & Bioconda`_,
   the explicit selection of the ``bioconda`` channel by means of the ``-c``
   option of ``conda install`` (e.g., ``conda install -c bioconda ...``)
   triggers a dependency error. DO NOT USE the ``-c bioconda`` option,
   just run ``conda install ...`` instead, as explained in the main text.

.. note::

   At the time of this writing, :ref:`SMRT LINK` does not contain the ``blasr``
   executable.


Using blasr from `sm-analysis`
------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/dave/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/dave/miniconda3

then, after activating the |project|'s virtual environment:

.. code-block:: console

   $ source /home/dave/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``blasr`` by using a command
line option (:option:`sm-analysis -b`) as follows:

.. code-block:: console

   $ sm-analysis --blasr-path /home/dave/miniconda3/bin/blasr


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels
