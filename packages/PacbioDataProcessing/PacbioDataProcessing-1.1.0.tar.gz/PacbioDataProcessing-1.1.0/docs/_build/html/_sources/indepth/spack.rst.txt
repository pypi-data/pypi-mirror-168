.. highlight:: shell

.. _using-spack:

Using Spack
===========

`Spack`_ is a package manager designed for large multi-user systems,
like clusters or supercomputers. One of its virtues is its simplicity
of usage. Chances are that if you are working with a cluster or a
supercomputer, `Spack`_ can help you get the work done when it comes
to installing software.

There is plenty of useful information in the official `Spack`_
documentation as well as in the `Spack tutorial`_. Some cluster admins
also have specific instructions on how to properly configure Spack in
their environment (like the `instructions to use spack at Goethe-HLR`_).

Therefore, we are not repeating that here. However in this document
you will find some very basic *recipes* to help you in the process of
installing |project| on a cluster.


Installing a compiler with Spack
--------------------------------

Once Spack is properly installed, it can be used to install a specific
compiler. To install ``gcc-11.3`` you can simply run:

.. code-block:: console

   $ spack install gcc@11.3

(Of course, other versions can be chosen, eg. ``gcc@9.3``).

It will be probably a long process, but it should be smooth... hopefully.
At the end Spack will tell you that there is a new module available to use
the compiler, if you like. In my case it is called
``gcc-11.3.0-gcc-8.2.0-qynjstf`` and it could be *loaded* with:

.. code-block:: console

   $ module load gcc-11.3.0-gcc-8.2.0-qynjstf

That will make the compiler *visible* within the current shell session:

.. code-block:: console

   $ gcc --version
   gcc (GCC) 11.3.0
   Copyright (C) 2021 Free Software Foundation, Inc.
   This is free software; see the source for copying conditions.  There is NO
   warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


.. admonition:: Adding a compiler to your Spack

   If you want to *add* the compiler to your Spack installation, such that
   the newly added compiler can be selected to compile new software with
   Spack, some configuration is needed (have a look at the `Spack`_
   documentation for details). After installing the compiler (the
   ``spack install gcc...`` line above), you can add the compiler with:

   .. code-block:: console

      $ spack compiler add $(spack location -i gcc@11.3.0)

   Now the installation of some software using that compiler could be done with

   .. code-block:: console

      $ spack install python@3.9%gcc@11.3


.. _`Spack`: https://spack.readthedocs.io/
.. _`Spack tutorial`: https://spack-tutorial.readthedocs.io/
.. _`instructions to use spack at Goethe-HLR`: https://csc.uni-frankfurt.de/wiki/doku.php?id=public:usage:spack
