.. highlight:: shell

.. _setting_up_bioconda:

Setting up Bioconda
===================

Probably the easiest (but not the only) way to install some external tools
required by |project|, like :ref:`pbindex <about-pbindex>`,
:ref:`blasr <about-blasr>` and :ref:`ccs <about-ccs>`,
is through `conda`_. If you decide to follow this route, this section
can hopefully help you.

The complete instructions can be found in `PacBio & Bioconda`_ and the
links therein, but they basically amount to:

1. Install ``conda``. See `installing conda`_ for full details, but it is
   probably enough to use `Miniconda`_, a minimal ``conda`` installer.
   In that case we will assume, as an example, that the ``conda`` environment
   is installed in a directory called::

     /home/dave/miniconda3

   .. warning::

      Depending on the choices made during the process of installing
      ``Miniconda`` you may allow the installer to configure your shell
      such that it *always* activates the ``conda`` environment at login
      time. If that is the case, and you are using :term:`Bash`, you will
      find in your :term:`Bash` initialization file , ``~/.bashrc``, a block
      similar to the following one:

      .. code-block:: console

	 # >>> conda initialize >>>
	 # !! Contents within this block are managed by 'conda init' !!
	 __conda_setup="$('/home/dave/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
	 if [ $? -eq 0 ]; then
             eval "$__conda_setup"
	 else
	     if [ -f "/home/dave/miniconda3/etc/profile.d/conda.sh" ]; then
                 . "/home/dave/miniconda3/etc/profile.d/conda.sh"
	     else
		  export PATH="/home/dave/miniconda3/bin:$PATH"
	     fi
	 fi
	 unset __conda_setup
	 # <<< conda initialize <<<

      Since we are using the ``conda`` environment in a very limited way,
      you can comment that block, prepending a ``#`` to each line.
      
2. Setup the ``channels`` in the ``conda`` environment just created as
   described in `Bioconda`_.
3. DO NOT run ``conda update --all``. The `PacBio & Bioconda`_ site strongly
   advises to do it, but that results in an environment where
   :ref:`pbindex <about-pbindex>`, :ref:`blasr <about-blasr>` and
   :ref:`ccs <about-ccs>` **cannot** be installed.

Obviously, for the purpose of having |project| up and running,
it is not necessary to install multiple conda environments to have
:ref:`pbindex <about-pbindex>`, :ref:`blasr <about-blasr>` and
:ref:`ccs <about-ccs>`.
The three tools can be installed in the same `conda`_ environment.


Using a conda environment
=========================

In some regards, a conda environment is very similar to a *normal*
:ref:`Python virtual environment <virtual environments>`. This implies,
as explained before, that you don't need to create one conda environment
for each package.

Apart from the instructions to deactivate the environment, what follows
is applicable to both conda environments and
:ref:`Python virtual environments <virtual environments>`.

To implicitly operate on a given conda environment, as it happens with Python
virtual environments, it must be activated.

Once the environment is created, if can be *activated* with:

.. code-block:: console

   $ source /home/dave/miniconda3/bin/activate

and the executables installed in it are visible without further ado. Just
type the name of the executable inside the environment to run it. For
instance, you would invoke the ``ccs`` executable simply typing it.

To *deactivate* a conda environment, run:

.. code-block:: console

   $ conda deactivate

However the activate/deactivate dance is not necessary if all
you want is to simply leverage one executable installed in a given
conda/virtual environment. Say that you want to run an executable called
``great-tool`` installed in the conda environment that we created under
``/home/dave/miniconda3``. It could be ``blasr``, ``pbindex`` or ``ccs``,
for instance. *With* or *without* activating the environment, the command
can be called giving its full path. This line:

.. code-block:: console

   $ /home/dave/miniconda3/bin/great-tool

would run the executable of interest.


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`Bioconda`: https://bioconda.github.io/#usage
.. _`installing conda`: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _`conda`: https://docs.conda.io
.. _`Miniconda`: https://docs.conda.io/en/latest/miniconda.html
