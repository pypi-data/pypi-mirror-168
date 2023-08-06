.. highlight:: shell

Glossary
========

.. glossary:: :sorted:

   molecule
     In the context of |project| *molecule* refers to a fragment of DNA that
     was captured in a hole, aka ZMW, in the sequencing machine. Each molecule
     in a BAM file is identified with a positive integer and typically spans
     several :term:`subreads <subread>`.

   subread
     A single line in the BAM file. Each subread belongs to one :term:`molecule`.

   summary report
     An HTML file created by :ref:`sm-analysis` with basic statistics about
     the input BAM, the input reference and the output produced by the
     :ref:`sm-analysis <sm-analysis>` program during its analysis. It includes
     also some intermediate details of the process and selected plots that provide
     a visual help for some quantities or additional information about a
     certain distribution or quantity.

   reference
     A DNA sequence used as a reference for the single molecule analysis stored
     as a file in the :term:`FASTA` format.

   FASTA
     Text based file format to store sequences of DNA, or in general, nucleotides
     or amino acids. See the `Wikipedia page on FASTA format`_, and references
     therein.

   alignment variant
     The result of aligning a BAM file using a *rotated reference*. The word
     *rotated* implies that the :term:`reference` is considered to have a
     circular topology (unless, of course, the angle of the rotation is ``0``).
     If the rotation angle is ``0`` degrees/radians, i.e. no rotation is
     applied to the reference, the result of the alignment is called *straight*
     in |project|. If a rotation angle of ``180`` degrees (or ``π`` radians) is
     applied to the refereence, the resulting alignment is called *pi-shifted*,
     or *π-shifted*.

   variant
     See :term:`alignment variant`.

   MD5 checksum
     A `checksum`_ based on the `MD5`_ algorithm. Used only in |project| as a
     mechanism to protect the data integrity against unintentional corruption.

   CSV file
     A *Comma Separated Values* file. As its name suggests, the file is
     structured in a table-like fashion, but, interestingly, the separator must
     not be a *comma*, although the comma is a very common choice. The CSV
     standard is defined in `RFC 4180`_.

   Command Line Interface (CLI)
     An interface between a system and its user based on the *command line*, i.e.
     the system's behaviour is controled by instructions passed to it as text
     through the keyboard. See `Command Line Interface (CLI)`_.

   Command Line Option
     A *flag* that can be used in a :term:`Command Line Interface (CLI)` to
     customize the behaviour of the program. In Unix a *command line option*
     typically begins by either ``-`` for short option names, e.g. ``-h`` or
     by ``--`` for long option names, e.g. ``--help``. A *command line option*
     might accept a value, e.g. ``-N 3``. That depends on the nature of the
     option.

   Graphical User Interface (GUI)
     An interface between a system and its user based on graphical icons, where
     the *mouse* is typically involved. See `Graphical User Interface (GUI)`_.

   GFF
     A file format to encode genetic features. See the `GFF3`_ definition.

   Bash
     The default `shell`_ of a GNU operating system, as its documentation
     declares. If the target OS is Linux, `Bash`_ is probably the `shell`_,
     or command line interface, that you are using to enter commands.
     In case of doubt, type:

     .. code-block:: console

	$ echo $SHELL

     and if you are using a ``bash`` shell you will get ``/bin/bash``.

   PATH
     An environment variable that contains the search path for commands.
     It is a colon-separated list of directories in which the shell looks
     for commands. Type ``man bash`` or ``info bash`` in your shell for more
     details.

   exit status
     The exit status of an executed command is the value returned by it (actually,
     by a ``waitpid`` system call or equivalent function). From the shell, the ``$?``
     variable holds the value returned by the last executed command. Type ``echo $?``
     *right after* the command you are interested in terminates, to find out its
     exit status. The exit statuses are integers in the range ``0-255``. A
     value of ``0`` means success. Non-zero values indicate failure.

   module
     In the context of a cluster, a ``module`` usually refers to a so-called
     *environment module*. It is a relatively low-level administrative tool to
     automate the steps required to use software installed in a non-standard location.
     Sometimes the term *modulefile* is used too, because
     it is a file, the *modulefile*, that defines the necessary modifications of
     the *environment* to enable a straightforwad usage of a particular piece of
     software that you are interested in. A module can be loaded (to add or make
     accessible the target software in the current environment) and unloaded (to
     remove it from the current environment). Environment modules give great
     flexibility to use software on a system that is not under your complete control
     (like a cluster): multiple implementations of the same facilities can coexist
     in the same system without conflicts, and without interfering with the base
     system. In a cluster, *modules* are typically loaded for instance, to use
     some compiler (version) or some library (version) or any other tool that is
     not available in the base system. See `environment modules`_
     or an introductory `article in Admin magazine on environment modules`_.

   CPython
     Python is a programming language with multiple *implementations*.
     Its reference implementation is written in the ``C``
     programming language and its name is ``CPython``. There are
     other implementations like `RustPython`_ (Python implemented
     in ``Rust``) or `PyPy`_ (Python implemented in ``RPython``), for instance.
     All implementations should be equivalent in functionality. Sometimes
     the term ``Python`` is used instead of ``CPython``. Though imprecise, this
     is common practice, if there is no confusion.


.. _`Wikipedia page on FASTA format`: https://en.wikipedia.org/wiki/FASTA_format
.. _`MD5`: https://en.wikipedia.org/wiki/MD5
.. _`checksum`: https://en.wikipedia.org/wiki/Checksum
.. _`RFC 4180`: https://datatracker.ietf.org/doc/html/rfc4180.html
.. _`Command Line Interface (CLI)`: https://en.wikipedia.org/wiki/Command-line_interface
.. _`Graphical User Interface (GUI)`: https://en.wikipedia.org/wiki/Graphical_user_interface
.. _`GFF3`: https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
.. _`Bash`: https://www.gnu.org/software/bash/
.. _`shell`: https://en.wikipedia.org/wiki/Unix_shell
.. _`environment modules`: http://modules.sourceforge.net/
.. _`article in Admin magazine on environment modules`: https://www.admin-magazine.com/HPC/Articles/Environment-Modules
.. _`RustPython`: https://rustpython.github.io/
.. _`PyPy`: https://www.pypy.org/
