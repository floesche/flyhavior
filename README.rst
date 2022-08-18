=========
flyhavior
=========


.. image:: https://img.shields.io/pypi/v/flyhavior.svg
        :target: https://pypi.python.org/pypi/flyhavior

.. image:: https://img.shields.io/travis/floesche/flyhavior.svg
        :target: https://travis-ci.com/floesche/flyhavior

.. image:: https://readthedocs.org/projects/flyhavior/badge/?version=latest
        :target: https://flyhavior.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Flyhavior is the basis for analyzing fly behavior data.


* Free software: MIT license
* Documentation: https://flyhavior.readthedocs.io.


Features
========

The current version of flyhavior merges data collected for the same experiment through the applications FlyFlix_ and FicTrac_. It takes the data collected by FlyFlix in a ``*.csv`` file and finds corresponding timestamps in the ``*.dat`` file of FicTrac. It then merges the two datasets into an experiment data format (see `Output format`_).

Usage
=====

To run flyhavior, you need to install the code, install dependencies, and choose the right branch for your raw data. Once you have generated the output file, an understanding of the output format will help to visualize and run statistics on the collected data.

Installing the code and dependencies
------------------------------------

Please download the software through GiHub, either by `cloning the repository <Flyhavior_>`_ or by choosing to `download and unpacking a zip file <Flyhavior zip_>`_ through the Code button.

Once you have downloaded the code it is highly recommended to `create a python virtual environment <venv_>`_ for this code.

To install all the dependencies required for the software to work refer to the ``requirements_dev.txt`` file.


_`Output format`
-------------

The output format is a single file that contains all experiment related data. Technically it is a SQLite_ file and any SQLite client can open the file.


Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _FlyFlix: https://github.com/floesche/FlyFlix
.. _FicTrac: https://github.com/floesche/fictrac
.. _Flyhavior: https://github.com/floesche/flyhavior
.. _Flyhavior zip: https://github.com/floesche/flyhavior/archive/refs/heads/main.zip
.. _venv: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
.. _SQLite: https://www.sqlite.org