.. highlight:: shell

.. _about-pbindex:

Pbindex
=======

The :ref:`sm-analysis program <sm-analysis>` delegates the indexing of
one-molecule BAM files to ``pbindex``, which must be accessible at runtime.
By default, ``pbindex`` is searched for in the :term:`PATH`. If it is
not found in the :term:`PATH`, you will receive an informative runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'pbindex'

and the :ref:`sm-analysis program <sm-analysis>` itself will stop.

In that case, the instructions in the following sections can help you.


Installing Pbindex
------------------

``pbindex`` is provided by the `pbbam`_ package.
A simple way to install `pbbam`_ is with ``conda``.
Have a look at :ref:`setting_up_bioconda`, and follow the instructions in there
if you want to choose the *conda route*. Once those steps are followed,
and the resulting ``conda`` environment is *active*, install ``pbbam``:

.. code-block:: console

   $ conda install pbbam

Upon success, you will be able to pass the path to the ``pbindex``
executable to :ref:`sm-analysis <sm-analysis>` if needed (see below how).

.. warning::

   Notice that, contrary to the suggestion given in `PacBio & Bioconda`_,
   the explicit selection of the ``bioconda`` channel by means of the ``-c``
   option of ``conda install`` (e.g., ``conda install -c bioconda ...``)
   triggers a dependency error. DO NOT USE the ``-c bioconda`` option,
   just run ``conda install ...`` instead, as explained in the main text.

.. note::

   An alternative way to install ``pbindex`` is through :ref:`SMRT LINK`.

Using Pbindex from `sm-analysis`
--------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/dave/.venvs/pdp

and let us assume that ``pbbam`` was installed in::

  /home/dave/miniconda3

then, after activating the |project|'s virtual environment:

.. code-block:: console

   $ source /home/dave/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``pbindex`` by using a command
line option (:option:`sm-analysis -p`) as follows:

.. code-block:: console

   $ sm-analysis --pbindex-path /home/dave/miniconda3/bin/pbindex

.. _`pbbam`: https://github.com/PacificBiosciences/pbbam
.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
