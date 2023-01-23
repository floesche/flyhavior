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
--------

Flyhavior currently merges [FlyFlix](https://github.com/floesche/FlyFlix) and [FicTrac](https://github.com/floesche/fictrac) data files into a SQLite3 file.

You can run flyhavior with the following command:

.. code:: bash

  python flyhavior/cli.py --flyflix <PATH_TO_FLYFLIX_CSV> --fictrac <PATH_TO_FICTRAC_DAT>


If you add the command line switch ``--post``, flyhavior creates a useful view ``v_move`` across all the tables and the helper table ``a_condition``.


SQLite tables
-------------

The generated experimental data file contains tables for different entities of the experiment, such as the ball, the fly, the experiment etc. There is also a view marked with the prefix `v_` that includes a subset of data columns useful for analysis. Use SQLite commands to explore and navigate the content of the tables.

Install
-------

1. clone this repository and change to this branch
2. create a new virtual environment for python and change to that environment
3. install dependencies via ``make install-dependencies``
4. copy the file ``load-data.mk.example`` to ``.load-data.mk``


Example run
-----------

1. after installing run ``make load-data``

This creates an SQLite3 file ``data/cshl001.db`` with all the experimental data.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
