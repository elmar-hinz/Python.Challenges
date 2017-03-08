==================
README: Challenges
==================

Library to assist programming, testing and execution of solutions for coding
challenges like those on stepik.org

A Minimal Hello World Class <Add>
=================================

.. code-block:: python

    from challenges.challenge import Challenge

    class Add(Challenge):
        sample = '''
            5, 6
        '''

        def build(self):
            self.model = self.line_to_integers(0)

        def calc(self):
            self.result = self.model[0] + self.model[1]

The class to write lets you focus on the core algorithms of the challenge while keeping stuff like opening, reading and
writing of files out of the way. You inherit several methods to set up the model or to format your result for writing.

While the class variable `sample` just holds a minimal example of the input, the actual input is later injected by
the **Challenge Runner** via the command line. In Bioinformatics this is often a large file of DNA.

.. hint:: See a more verbose example of HelloWorld.

    * https://github.com/elmar-hinz/Python.Challenges/blob/master/HelloWorld/HelloWorld.py
    * https://github.com/elmar-hinz/Python.Challenges/blob/master/HelloWorld/HelloWorldTestCase.py


The Challenge Runner Supports the Following Features
====================================================

    * Listing available challenges
    * Scaffolding a new challenge directory, with a challenge class and a unit test class
    * Executing the small `sample` within the challenge class
    * Reading input files from the command line
    * Result output on the command line
    * Writing `sample.txt` and matching `result.txt` into the challenges directory
    * Running the unit test case of a challenge

The Layout of Your Directory Looks Like This
============================================

.. code-block:: bash

    myChallenges/
        Challenge1/Challenge1.py
        Challenge1/Challenge1TestCase.py
        Challenge2/Challenge2.py
        Challenge2/Challenge2TestCase.py
        ... more challenges ...

The names `Challenge1` and `Challenge2` are just placeholders for the names you choose during scaffolding.

Running the Challenge Runner
============================

The directory `myChallenges/` is the base directory of your challenges project. It's the directory from where to use the
**Challenge Runner**.


List the Available Challenges
-----------------------------

.. code-block:: bash

    prompt> challenge --list
    * Challenge1
    * Challenge2
    * ...

Scaffolding a New Challenge
---------------------------

.. code-block:: bash

    prompt> challenge --scaffold Challenge3

You now find the files:

.. code-block:: bash

    myChallenges/
        Challenge3/Challenge3.py
        Challenge3/Challenge3TestCase.py

Check it's working by running the unit test case.

.. code-block:: bash

    prompt> challenge --unittest Challenge3
    ...
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK

Run <sample> from the Class File
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


Read Sample from an Input File
------------------------------

.. code-block:: bash

    prompt> challenge Challenge1 --file ~/Downloads/data.txt
    [the result output goes here]

Storing Data and Results
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

Naming Conventions
==================

The naming conventions follow the standards as defined by **PEP 8 -- Style Guide for Python Code**

https://www.python.org/dev/peps/pep-0008/

There are two deliberate exceptions:

1. Challenge module names are **CamelCase**:

    In contradiction to the style guide directory and class file of the challenges are not all lowercase. Especially the
    first character must be uppercase. This is used to find and list the challenge directories between other modules.
    Even more, the directory, the class file and the class name must all use the same word, with the `.py` extension for
    the file.

2. Inherited class attributes and methods don't have a leading underscore:

    The inherited functions and methods of the challenge are not a public API and the style guides recommends leading
    underscores. As inheritance is a core concept of the challenge class, this would lead to a hell of leading
    underscores. For this reason we don't follow the style guide in this recommendation.

Installation
============

.. important::

    This solftware requieres Python 3.

Clone from Github
-----------------

You can clone (or download) the Challenges project directly from Github. In this case the scripts and pathes are not
configured globally. Either you configure it globally or you place your challenges immediately into the projects folder
so that the paths are detected relatively.

Put Your Challenges Immediately Into the Projects Folder
........................................................

This is the most simple setup to get started. After downloading change into the download folder an try to run the
`HelloWorld` unit test. In this case the command is in the `bin` directory, you call it as `bin/challenge`.

.. code-block:: bash

    prompt> bin/challenge -u HelloWorld
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK

Now you are ready to create your challenge side-by-side with the `HelloWorld` challenge.

.. code-block:: bash

    prompt> bin/challenge -s MyChallenge

Use <pip> to Install <challenges>
---------------------------------

If you have a fully configured python 3 environment up and running you can install <challenges> with pip3.

.. code-block:: bash

    prompt> pip3 search challenges
    prompt> pip3 install challenges

The library will be included into the python class path. The runner will be globally available as `challenge` or
alternatively as `stepik`.

.. code-block:: bash

    prompt> challenge -V
    challenge 0.1.2

    prompt> stepik -V
    stepik 0.1.2



