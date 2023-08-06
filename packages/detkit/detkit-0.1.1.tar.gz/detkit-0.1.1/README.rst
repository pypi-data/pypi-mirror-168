******
detkit
******

|travis-devel| |codecov-devel| |licence| |format| |pypi| |implementation| |pyversions|

A python package to compute common determinant functions in machine leanring.

.. For users
..     * `Documentation <https://ameli.github.io/detkit/index.html>`_
..     * `PyPi package <https://pypi.org/project/detkit/>`_
..     * `Source code <https://github.com/ameli/detkit>`_
..
.. For developers
..     * `API <https://ameli.github.io/detkit/_modules/modules.html>`_
..     * `Travis-CI <https://travis-ci.com/github/ameli/detkit>`_
..     * `Codecov <https://codecov.io/gh/ameli/detkit>`_

+----------------------------------------------------------------+-----------------------------------------------------------------+
|    For users                                                   | For developers                                                  |
+================================================================+=================================================================+
| * `Documentation <https://ameli.github.io/detkit/index.html>`_ | * `API <https://ameli.github.io/detkit/_modules/modules.html>`_ |
| * `PyPi package <https://pypi.org/project/detkit/>`_           | * `Travis-CI <https://travis-ci.com/github/ameli/detkit>`_      |
| * `Anaconda Cloud <https://anaconda.org/s-ameli/detkit>`_      | * `Codecov <https://codecov.io/gh/ameli/detkit>`_               |
+----------------------------------------------------------------+-----------------------------------------------------------------+

*******
Install
*******

Install by either of the following ways:

* **Method 1:** The recommended way is to install through the package available at `PyPi <https://pypi.org/project/detkit>`_:

  ::

    python -m pip install detkit

* **Method 2:** Install through the package available at `Anaconda <https://anaconda.org/s-ameli/detkit>`_:

  ::

    conda install -c s-ameli detkit


* **Method 3:** download the source code and install by:

  ::

    git clone https://github.com/ameli/detkit.git
    cd detkit
    python -m pip install -e .


.. ********
.. Citation
.. ********
..
.. .. [Ameli-2020] Ameli, S., and Shadden. S. C. (2020). Interpolating the Trace of the Inverse of Matrix **A** + t **B**. `arXiv:2009.07385 <https://arxiv.org/abs/2009.07385>`__ [math.NA]
..
.. ::
..
..     @misc{AMELI-2020,
..         title={Interpolating the Trace of the Inverse of Matrix $\mathbf{A} + t \mathbf{B}$},
..         author={Siavash Ameli and Shawn C. Shadden},
..         year={2020},
..         month = sep,
..         eid = {arXiv:2009.07385},
..         eprint={2009.07385},
..         archivePrefix={arXiv},
..         primaryClass={math.NA},
..         howpublished={\emph{arXiv}: 2009.07385 [math.NA]},
..     }
..

.. ****************
.. Acknowledgements
.. ****************
..
.. * American Heart Association #18EIA33900046

.. |examplesdir| replace:: ``/examples`` 
.. _examplesdir: https://github.com/ameli/detkit/blob/main/examples
.. |example1| replace:: ``/examples/Plot_detkit_FullRank.py``
.. _example1: https://github.com/ameli/detkit/blob/main/examples/Plot_detkit_FullRank.py
.. |example2| replace:: ``/examples/Plot_detkit_IllConditioned.py``
.. _example2: https://github.com/ameli/detkit/blob/main/examples/Plot_detkit_IllConditioned.py
.. |example3| replace:: ``/examples/Plot_GeneralizedCorssValidation.py``
.. _example3: https://github.com/ameli/detkit/blob/main/examples/Plot_GeneralizedCrossValidation.py

.. |travis-devel| image:: https://img.shields.io/travis/com/ameli/detkit
   :target: https://travis-ci.com/github/ameli/detkit
.. |codecov-devel| image:: https://img.shields.io/codecov/c/github/ameli/detkit
   :target: https://codecov.io/gh/ameli/detkit
.. |licence| image:: https://img.shields.io/github/license/ameli/detkit
   :target: https://opensource.org/licenses/BSD-3-Clause
.. |travis-devel-linux| image:: https://img.shields.io/travis/com/ameli/detkit?env=BADGE=linux&label=build&branch=main
   :target: https://travis-ci.com/github/ameli/detkit
.. |travis-devel-osx| image:: https://img.shields.io/travis/com/ameli/detkit?env=BADGE=osx&label=build&branch=main
   :target: https://travis-ci.com/github/ameli/detkit
.. |travis-devel-windows| image:: https://img.shields.io/travis/com/ameli/detkit?env=BADGE=windows&label=build&branch=main
   :target: https://travis-ci.com/github/ameli/detkit
.. |implementation| image:: https://img.shields.io/pypi/implementation/detkit
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/detkit
.. |format| image:: https://img.shields.io/pypi/format/detkit
.. |pypi| image:: https://img.shields.io/pypi/v/detkit
