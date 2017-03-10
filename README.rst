
==================
README: Challenges
==================

Library to assist programming, testing and execution of solutions for coding
challenges like those on stepik.org

Find the full documentation at Readthedocs_.

.. _Readthedocs: http://challenges.readthedocs.io

:State: alpha
:License: MIT
:Author: Elmar Hinz
:Repository: https://github.com/elmar-hinz/Python.Challenges
:Documentation Server: http://challenges.readthedocs.io |badge|

.. |badge| image:: https://readthedocs.org/projects/challenges/badge/?version=latest
    :target: http://challenges.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Hello world
===========

.. code-block:: python

    from challenges import Challenge

    class AddChallenge(Challenge):
        sample = '''
            5, 6
        '''

        def build(self):
            self.model = self.line_to_integers(0)

        def calc(self):
            self.result = self.model[0] + self.model[1]

The class to write lets you focus on the core algorithms of the challenge while keeping stuff like opening, reading and
writing of files out of the way. You inherit several methods to set up the model or to format your result for writing.

While the class attribute `sample` just holds a minimal example of the input, the actual input is later injected by
the **Challenge Runner** via the command line. In Bioinformatics this is often a large file of DNA.

.. hint:: See a more verbose example of HelloWorld.

    * HelloWorldChallenge_
    * HelloWorldTest_

.. _HelloWorldChallenge: https://github.com/elmar-hinz/Python.Challenges/blob/master/HelloWorld/challenge.py
.. _HelloWorldTest: https://github.com/elmar-hinz/Python.Challenges/blob/master/HelloWorld/test.py

Features
========

    * Listing available challenges
    * Scaffolding a new challenge directory with a challenge class and a unit test class
    * Executing the `sample` from the sample class attribute
    * Reading input files from the command line
    * Output formatted result on the command line
    * Writing `sample.txt` and matching `result.txt` into the challenges directory
    * Running the unit test case of a challenge

Directory layout
================

.. code-block:: bash

    anyDirectory/
        Challenge1/challenge.py
        Challenge1/test.py
        Challenge2/challenge.py
        Challenge2/test.py
        ... more challenges ...

The names `Challenge1` and `Challenge2` are just placeholders for the names you choose during scaffolding.

Challenge runner
================

The directory `myChallenges/` is the base directory of your challenges project. It's the directory from where to use the
**Challenge Runner**.

List the available challenges
-----------------------------

.. code-block:: bash

    prompt> challenge --list
    * Challenge1
    * Challenge2
    * ...

Scaffolding a new challenge
---------------------------

.. code-block:: bash

    prompt> challenge --scaffold Challenge3

You now find the files:

.. code-block:: bash

    myChallenges/
        Challenge3/challenge.py
        Challenge3/test.py

Check it's working by running the unit test case.

.. code-block:: bash

    prompt> challenge --unittest Challenge3
    ...
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK

Run <sample> from the class file
--------------------------------

This is the small sample directly coded into the challenge class.

.. code-block:: bash

    prompt> challenge --klass Challenge1
    [the result output goes here]

.. hint::

    You will automatically find the latest output in two files, independent from the input method you choose.

    .. code-block:: bash

        myChallenges/Challenge1/latest.txt
        myChallenges/latest.txt

    These files are just for convenience and are overwritten by the next run.


Read sample from an input file
------------------------------

.. code-block:: bash

    prompt> challenge Challenge1 --file ~/Downloads/data.txt
    [the result output goes here]

Storing data and results
------------------------

Did you pass the challenge? Was the online grader content with the upload of `latest.txt`? Then you should store data
and result.

.. code-block:: bash

    prompt> challenge Challenge1 --file ~/Downloads/data.txt --write

You will find the files:

.. code-block:: bash

        myChallenges/Challenge1/sample.txt
        myChallenges/Challenge1/result.txt

This files are stored until the next run with the `--write` flag.

Help
----

To quickly see all available options.

.. code-block:: bash

    challenge --help

Naming conventions
==================

The naming conventions follow the standards as defined by `PEP 8`_ **Style Guide for Python Code**

.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/

There are two deliberate exceptions:

1. Challenge module names are **CamelCase**:

    In contradiction to the style guide directories of the challenges are not all lowercase. Especially the
    first character must be uppercase. This is used to find and list the challenge directories between other modules.
    If the name of your challenge is **ExampleProblem** then this are the required names:

    :Directory: ``ExampleProblem/``
    :Challenge file: ``ExampleProblem/challenge.py``
    :Unittest file: ``ExampleProblem/test.py``
    :Full qualified challenge class: ``ExampleProblem.challenge.ExampleProblemChallenge``
    :Full qualified test class: ``ExampleProblem.test.ExampleProblemTest``

    This is automatially wired up during scaffolding.

2. Inherited class attributes and methods don't have a leading underscore:

    The inherited functions and methods of the challenge are not a public API and the style guides recommends leading
    underscores. As inheritance is a core concept of the challenge class, this would lead to a hell of leading
    underscores. For this reason we don't follow the style guide in this recommendation.

.. tip::

    On useful advantage of naming the directory just like your challenge is, that you can use the path expansion
    mechanism of the shell. Write the first characters of the directory name and hit <TAB>. Now you can use the
    directory name as name of the challenge. A trailing slash is discarded. The following two inputs are equivalent.

    .. code-block:: bash

        prompt> challenge -k ExampleProblem
        prompt> challenge -k ExampleProblem/

Installation
============

.. important::

    This software requires Python 3.

Clone from Github
-----------------

You can clone (or download) the Challenges project directly from Github. In this case the scripts and paths are not
configured globally. Either you configure it globally or you place your challenges immediately into the projects folder
so that the paths are detected relatively.

Put your challenges immediately into the projects folder
........................................................

This is the most simple setup to get started. After downloading change into the download folder an try to run the
`HelloWorld` unit test. In this case the command is in the `bin` directory, you call it as `bin/challenge`.

.. code-block:: bash

    prompt> bin/challenge --unittest HelloWorld
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK

Now you are ready to create your challenge side-by-side with the `HelloWorld` challenge.

.. code-block:: bash

    prompt> bin/challenge --scaffold MyChallenge

Use <pip> to install <challenges>
---------------------------------

If you have a fully configured python 3 environment up and running you can install <challenges> with pip3.

.. code-block:: bash

    prompt> pip3 search challenges
    prompt> pip3 install challenges

The library will be included into the python class path. The runner will be globally available as `challenge` or
alternatively as `stepik`.

.. code-block:: bash

    prompt> challenge --version
    challenge 0.1.2

    prompt> stepik --version
    stepik 0.1.2


