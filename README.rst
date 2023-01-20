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

The generated experimental data file contains the following tables and values. This is just an incomplete snapshot, refer to the database schema for the actual data.

ball
        ball number and weight.
fly
        fly number, sex, birth_after, birth_before, strain, batch, day_start, day_end, and incubator_since
condition
        trial number, trial type, condition number, condition type, fps, bar_size, interval size, comment, repetition, gain, stimulus_type, start_orientation, left_right, fg_color, bg_color, contrast, and brightness
experiment
        start, end, temperature, air, glue, distance, display, display_brightnesss, display_color, ball, fly, starvation_start, tether_start, tether_end, and protocol
fictrac
        frame_counter, experiment, d_cam_x, d_cam_y, d_cam_z, err, d_lab_x, d_lab_y, d_lab_z, cam_x, cam_y, cam_z, lab_x, lab_y, lab_z, integrated_lab_x, integrated_lab_y, animal_lab_heading, animal_lab_movement, animal_speed, integrated_movement_x, integrated_movement_y, timestamp, seq, delta_timestamp, and alternative_timestamp
schema
        client_ts_ms, fictrac_seq, fictrac_id, rendered, speed, and angle

v_move
        view that integrates the most important values from the above table into a single table/spreadsheet

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
