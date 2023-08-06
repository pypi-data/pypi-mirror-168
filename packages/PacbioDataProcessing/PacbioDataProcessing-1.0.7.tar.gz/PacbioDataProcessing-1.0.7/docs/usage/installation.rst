.. highlight:: shell

.. _installation:

Installation
============


Pre-requisites
--------------

Python
^^^^^^

To install **PacBio Data Processing** a Python interpreter is needed
in your system since the package is written in Python. The recommended
version of Python is ``3.9``. Strictly speaking the code should work
with a less recent version, but some dependencies will require anyway
``Python-3.9``.

.. note::

   Along this document we will show commands to be typed in a *terminal*.
   You will notice that the commands are preceeded by a ``$`` symbol
   that represents the *prompt*. The ``$`` SHOULD NOT be typed. Its
   purpose is to distinguish between commands to be typed and output,
   since outputs will NOT have a preceeding ``$`` symbol.

.. note::

   During the installation process you will type several shell commands. The
   typical behaviour of shell commands is quite *ingrate*: loud complains
   and quiet *celebrations*. What can you do to know if a command worked
   correctly or not? You can find the :term:`exit status` of the *latest*
   issued command with ``echo $?``. For instance:

   .. code-block:: console

      $ make
      ... lots of output ...
      $ echo $?
      0

   The displayed :term:`exit status` of ``0`` means that the program
   ``make`` ran  *successfully*.
      
If you are using Linux, it is likely that Python is
already present in your system. Open a terminal and check it out with:

.. code-block:: console

    $ python --version

or

.. code-block:: console

    $ python3 --version

You know that Python is in your system if you get as output something
like (your mileage may vary):

.. code-block:: console

    Python 3.9.13

.. admonition:: Installing Python

    If you don't have Python, or you have an old version, you can either
    use your system's package manager to install a recent version of Python,
    or visit the official `Python`_ site, where there is a link to
    `Download Python`_. Then install Python using the downloaded file.

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

    In case you need/want to learn more about the Python installation process
    in general, you might be interested in reading this
    `Python installation guide`_.


.. _other-dependencies:

Other dependencies
^^^^^^^^^^^^^^^^^^

**PacBio Data Processing** delegates some tasks to external tools.
Therefore, the next is a list of *external dependencies*:

- :ref:`kineticsTools`
- :ref:`pbindex <about-pbindex>`
- :ref:`blasr <about-blasr>`
- :ref:`ccs <about-ccs>`
- :ref:`about-htslib`

These dependencies **are required** to be present in your system in order
to use some tools provided by **PacBio Data Processing**. You need to
install them if they are absent in your system.


.. _virtual environments:

Virtual environment
^^^^^^^^^^^^^^^^^^^

It is *optional* but *highly recommended* to use a virtual environment
(or a variant thereof) to install **PacBio Data Processing**. In this
document we will use the standard library's ``venv`` module.

A virtual environment (or ``venv`` for short) allows us to have
the required set of packages independently of the system-wide packages
installed. This has several advantages. First, it will help you produce an
*isolated mess* in case something goes wrong, but it also allows us to
decide the version of any package we are interested in. irrespective
of what other ``venv``'s need, or what the system needs.

A ``venv`` can be created like follows:

.. code-block:: console

    $ python3.9 -m venv PDP-py39

this line will create a folder called ``PDP-py39`` containing the ``venv``.
You can choose another name if you like.
After the installation one can activate the ``venv`` to start using it with:

.. code-block:: console

    $ source PDP-py39/bin/activate

From that point on, the management of and access to Python packages 
happens *within* the ``venv``. For example, installing a new package
will be done inside the ``venv``.

Afterwards you can proceed with the installation of
**PacBio Data Processing**.

For more information on ``venv``'s, consult the documentation of that module
in the standard library `venvs`_, and references therein.

.. note::

   To stop using a ``venv``, type ``deactivate`` *in the same*
   terminal where the ``venv`` was activated.

.. _venvs: https://docs.python.org/3/library/venv.html


Installing the stable release of PacBio Data Processing
-------------------------------------------------------

The latest stable release of **PacBio Data Processing** can be installed
by executing this command in your terminal:

.. code-block:: console

    $ pip install PacbioDataProcessing

or, optionally, if you want to enable the ``sm-analysis-gui`` program,
i.e. the GUI to the single molecule analysis, running this:

.. code-block:: console

    $ pip install PacbioDataProcessing[gui]

However, be aware that the installation including the GUI will fail if
your system does not have [wxpython]_ installed.

.. note::

   In the rare case that you don't have `pip`_ installed, this
   `Python installation guide`_ can guide you through the process of
   installing pip.

.. note::

   Typically, after you use ``pip`` for the first time in your ``venv``
   you receive a warning message saying that your version of ``pip`` is too
   old::

     WARNING: You are using pip version 22.0.4; however, version 22.1.2 is available.
     You should consider upgrading via the '/path/to/your/venv/bin/python -m pip install --upgrade pip' command.

   That happens because the ``pip`` bundled with the specific version of Python
   you used to create the ``venv`` is older than the newest version available.
   You can update ``pip`` by following the command provided. Or, if the ``venv``
   is active, equivalently with:

   .. code-block:: console

      $ pip install -U pip

   that will *upgrade* ``pip`` and make the warning messages disappear.

.. _Python:  https://www.python.org/
.. _Download Python: https://www.python.org/downloads/
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Alternative: Installing PacBio Data Processing from a file
----------------------------------------------------------

It is also possible to install |project| from  a file: a
`tarball <https://en.wikipedia.org/wiki/Tar_(computing)>`_ or
a `wheel <https://pythonwheels.com/>`_.

You simply need the file and run pip on it. For instance, using as an example
a *tarball* corresponding to version ``1.0.0``, it would be:

.. code-block:: console

   $ pip install PacbioDataProcessing-1.0.0.tar.gz

From a wheel it would be:

.. code-block:: console

   $ pip install PacbioDataProcessing-1.0.0-py3-none-any.whl

Of course, you could also choose to install optional dependencies as usual:

.. code-block:: console

   $ pip install PacbioDataProcessing-1.0.0-py3-none-any.whl[gui]


Alternative: Installing PacBio Data Processing from the repository
------------------------------------------------------------------

.. warning::
   The instructions in this section are not necessary for
   end users. If you are simply interested in using
   **PacBio Data Processing** to analyze some BAM file
   or you need to use some functionality provided by
   **PacBio Data Processing** from within your code,
   you don't necessarily need this section.
   But if you want to have access to the source
   code keep reading.

The sources of **PacBio Data Processing** can be downloaded from its `GitLab repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://gitlab.com/dvelazquez/pacbio-data-processing

and install it with:

.. code-block:: console

    $ pip install ./pacbio-data-processing


**Or** download the tarball:

.. code-block:: console

    $ curl -JL https://gitlab.com/dvelazquez/pacbio-data-processing/-/archive/master/pacbio_data_processing-master.zip  --output pacbio-data-processing-master.zip

and install it with:

.. code-block:: console

    $ pip install pacbio-data-processing-master.zip

**Or** simply run:

.. code-block:: console

   $ pip install git+https://gitlab.com/dvelazquez/pacbio-data-processing


.. _GitLab repo: https://gitlab.com/dvelazquez/pacbio-data-processing

