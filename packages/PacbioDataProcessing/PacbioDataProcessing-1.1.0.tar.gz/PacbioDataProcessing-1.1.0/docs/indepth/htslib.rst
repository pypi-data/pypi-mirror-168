.. highlight:: shell

.. _about-htslib:

HTSlib
======

|project| uses `pysam`_, a wrapper around `HTSlib`_,
to read the BAM files. Although the installation of `pysam`_ is
automatically triggered by the installation of |project|,
`HTSlib`_ must be installed independently, otherwise |project|
will die at runtime.

Installing HTSlib
-----------------

In the sections below, I briefly explain two ways to install `HTSlib`_.


Standard installation
^^^^^^^^^^^^^^^^^^^^^

Probably, the easiest way to install `HTSlib`_ is through your package
manager. But it can be installed also from sources; have a look at the
`HTSlib`_ webpage to learn about that.


Spack
^^^^^

Another particularly simple way to install `HTSlib`_ is through
:ref:`Spack <using-spack>`, especially if you are going to work on a
cluster where using its package manager is cumbersome, or even impossible,
and the installation from sources is not appealing to you. In this case
the installation with :ref:`Spack <using-spack>` goes as follows.

1. (Optional) Choosing the compiler. `HTSlib`_ will be compiled from source
   code by :ref:`Spack <using-spack>`. You might need to choose an up-to-date
   compiler (clusters tend to have very stable, ie. old, default compilers).
   See :ref:`using-spack` for details.

2. Installing `HTSlib`_ itself. With the default compiler it would be:
   
   .. code-block:: console

      $ spack install htslib

   or if we want to install it with a specific compiler, say ``gcc-11.3``:

   .. code-block:: console

      $ spack install htslib%gcc@11.3

   The result will be a :term:`module`. In our case, the name of the
   :term:`module` is ``htslib-1.14-gcc-11.3.0-22tiwx3``

3. Using `HTSlib`_. As mentioned above, |project| depends on `HTSlib`_ at
   runtime. It means that after a successfull installation, the created
   :term:`module` must be loaded whenever it is needed:

   .. code-block:: console

      $ module load htslib-1.14-gcc-11.3.0-22tiwx3

   .. warning::

      Remember to add the line:

      .. code-block:: console

	 module load htslib-1.14-gcc-11.3.0-22tiwx3

      at the beginning of the slurm batch scripts used to submit any
      executable from |project|.


.. _`HTSlib`: https://www.htslib.org/
.. _`pysam`: https://pysam.readthedocs.io/
