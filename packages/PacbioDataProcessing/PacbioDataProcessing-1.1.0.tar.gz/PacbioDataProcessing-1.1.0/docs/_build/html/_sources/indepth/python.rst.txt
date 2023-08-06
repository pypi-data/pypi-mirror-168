.. highlight:: shell

.. _installing-python:

Installing Python
=================

There are multiple options to install Python. If you are working with
Linux, hopefully this document can help you. If you are working with
another OS or the instructions below do not help you, you can visit the
official `Python`_ site, where there is a link to `Download Python`_.
Then install Python using the downloaded file.

In case you need/want to learn more about the Python installation process
in general, you might be interested in reading this
`Python installation guide`_.

In Linux, if you have administration permissions, the easiest way to
install Python is through your system's package manager. How this can
be done is obviously outside the scope of this documentation.

If you don't have priviledges to install software on your target system
using the package manager (that is typically the case if you plan to run
|project| on a cluster), you still can easily use Spack to install Python.
Alternatively, you can also install Python directly from *sources*. In
the sections below these two options are described.


Default: installing Python with Spack
-------------------------------------

With Spack (see :ref:`using-spack` for details) the installation
of Python is straigthforward. Once Spack is on your system, which
doesn't require particular priviledges, run:

.. code-block:: console

   $ spack install python@3.9.13

to install ``CPython-3.9.13`` (see :term:`CPython`).

On success, Spack will inform you about the :term:`module` that has
been created and which must be *loaded* if you want to use it. In
my case the name of the module is ``python-3.9.13-gcc-9.5.0-oesebwh``,
hence, to use it:

.. code-block:: console

   $ module load python-3.9.13-gcc-9.5.0-oesebwh

YMMV. If you forget the name of the module, you can use the ``<TAB>`` to
autocomplete the line, or list all modules available in your system with:

.. code-block:: console

   $ module avail


Alternative: installing Python from sources
-------------------------------------------

.. warning::

   Use this option as a last resort, since you need to be able to
   install some libraries in order to produce a usable Python
   installation from the sources. If you cannot install Python with
   your package manager, you might expect problems getting Python
   up and running from sources...


If you download the *sources* (typically a file ending in ``.tgz``,
``.tar.xz`` or similar) the procedure is relatively simple:

1. *untar* the file. For instance:

   .. code-block:: console

      $ tar xf Python-3.9.13.tgz

2. Enter in the created directory with the sources:

   .. code-block:: console

      $ cd Python-3.9.13

3. Open the ``README.rst`` file and follow the instructions in its
   *Build Instructions* section. They schematically amount to 3 steps:

   .. code-block:: console

      $ ./configure
      $ make
      $ make install

   In the ``configure`` step you can customize various features of the
   compilation and installation process. For instance, two common options
   are ``--prefix`` (to install Python in a custom location and not in
   the default system-wide location) and ``--enable-optimizations``. The
   following command (to be executed before ``make``) would use both
   options:

   .. code-block:: console

      $ ./configure --prefix=/home/dave --enable-optimizations

   The given prefix (``/home/dave``) implies that the ``make install``
   step will create suitable directories under the given location to
   have the necessary structure to use Python. It is up to the user
   to leverage that installation. That could be as simple as calling
   python with the full (or relative) path to its interpreter, e.g. in
   the case of using ``--prefix=/home/dave``:

   .. code-block:: console

      $ /home/dave/bin/python3

   If you want to use the compiled interpreter as your default Python
   interpreter, modify the ``PATH`` shell variable to make the terminal
   aware of your recently installed Python:

   .. code-block:: console

      $ export PATH="/home/dave/bin:${PATH}"

   After that, the current shell and any subprocesses created from it, will
   know that by typing:

   .. code-block:: console

      $ python
      # or
      $ python3

   (or any other executable installed, check the contents of
   ``/home/dave/bin``) you mean actually ``/home/dave/bin/python`` or
   ``/home/dave/bin/python3``, etc.

   If you want this change to be permanent, i.e. if you don't want to type
   the complete path to your newly installed Python interpreter but you don't
   want to modify the ``PATH`` variable *every* time you log in, and you are
   using :term:`Bash`, add the ``export`` line above near the end of your
   ``.bashrc`` file (``/home/dave/.bashrc`` in our example);
   if ``.bashrc`` is missing in your home directory, feel free to create one.

   The CPython ``README.rst`` file is worth having a look for more insights
   about the options available for the manual installation of CPython. It
   contains very useful hints and a lot more information.

.. _Python:  https://www.python.org/
.. _Download Python: https://www.python.org/downloads/
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
