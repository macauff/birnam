************
Installation
************

Package Requirements
====================

Currently there are no strict criteria for installation; it is suggested that you use the most up-to-date package versions available. The one exception there is that the minimum version of Python is set to 3.8, and development is currently focused on Python 3.10+.

The current package requirements, and citations to give for use of ``birnam`` in your work where available, are:

* ``numpy`` -- Harris et al. 2020 (Nature, 585, 357)
* ``pandas`` -- The pandas development team 2020 (doi.org/10.5281/zenodo.3509134)
* ``scikit-build-core`` -- Schreiner et al. 2022 (doi.org/10.25080/majora-212e5952-033)
* ``cmake``.

For running the test suite the requirements are:

* ``tox``
* ``pytest``
* ``sphinx-fortran``
* ``sphinx-astropy``
* ``pytest-astropy``
* ``pytest-cov``
* ``isort``
* ``pylint``
* ``pre-commmit``.

Additionally, you will need the following to install ``birnam``:

* ``git``

Installing the Package
======================

As of now, the main way to install this package is by downloading it from the `GitHub repository <https://github.com/macauff/birnam>`_. We recommend using an `Anaconda Distribution <https://www.anaconda.com/distribution/>`_, or `miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, to maintain specific, independent Python installations without the need for root permissions.

Once you have installed your choice of conda, then you can create an initial conda environment::

    conda create -n your_environment_name -c conda-forge python=3.9 numpy pandas scikit-build-core cmake

although you can drop the ``=3.9``, or chose another (later) Python version -- remembering the minimum version is 3.8 -- if you desire to do so. Then activate this as our Python environment::

    conda activate your_environment_name

If you require the additional test packages listed above, for running tests, you can install them separately with::

    conda install -c conda-forge tox pytest sphinx-astropy pytest-astropy pytest-cov isort pylint pre_commit
    conda install -c vacumm -c conda-forge sphinx-fortran

Finally, install ``git`` if you do not have it on your computer; `instructions <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_ for installing it on your operating system are available.

Once you have the required packages installed -- whether in a new ``conda`` environment or otherwise -- you can clone the repository::

    git clone git://github.com/macauff/birnam.git

which will place the repository in the folder from which you invoked the ``git`` command. Now, from inside the folder that was just created (``cd birnam`` or equivalent), you can either run::

    pip install .

which will install ``birnam`` such that you can ``import birnam`` from other folders on your computer. However, if this is to develop the software, your changes will not be reflected in the installed version of the code (and you must re-install using the above command); if you wish to have ``Python`` code changes immediately reflected in your ``pip``-installed version of the software, you can install ``birnam`` using::

    pip install -e .

To confirm your installation was successful, you can ``import birnam`` in a Python terminal.

Testing
=======

To run the main unit test suite, assuming you installed it during the above process, you can run::

    tox -e test

If you wish to locally build the documentation -- mostly likely if you are improving or extending the documentation, as the docs are available online -- you can run::

    tox -e build_docs

To match the github actions ``pre-commit`` workflow, locally you can run::

    SKIP=check-lincc-frameworks-template-version,no-commit-to-branch,check-added-large-files,pytest-check,sphinx-build,pylint pre-commit run --show-diff-on-failure --color=always --all-files

which will run ``isort`` and report any issues with the formatting prior to code being merged into the main codebase.

Additionally, ``pylint`` can be invoked directly using::

    pylint -rn -sn --recursive=y ./src --rcfile=./src/.pylintrc
    pylint -rn -sn --recursive=y ./tests --rcfile=./tests/.pylintrc

to run the linter on each folder, with changes being manually made to comply with the reporting.

Getting Started
===============

Once you have installed the package, check out the :doc:`Quick Start<quickstart>` page.
