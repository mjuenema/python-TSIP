************
Contributing
************

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
======================

Report Bugs
-----------

Report bugs at https://github.com/mjuenema/python-TSIP/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
--------

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
------------------

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
-------------------

Python TSIP could always use more documentation, whether as part of the
official Python TSIP docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
---------------

The best way to send feedback is to file an issue at https://github.com/mjuenema/python-TSIP/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Get Started!
============

.. note:: Some of the steps described below may not work yet.

Ready to contribute? Here's how to set up `python-TSIP` for local development. Most of the commands
are accessible through the ``mMkefile``.

1. Install the gitflow_ Git add-on. Gitflow implements the work-flow described
   in `A successful Git branching model`_.

2. Fork the `python-TSIP` repo on GitHub.

3. Clone your fork locally::

    $ git clone git@github.com:your_name_here/python-TSIP.git

4. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv python-TSIP
    $ cd python-TSIP/
    $ python setup.py develop

5. Initialise Gitflow::

   $ git flow init -d

6. Start a new feature or branch::

    $ git flow feature start <name-of-your-feature>

   Now you can make your changes locally.

7. When you're done making changes, check that your changes pass flake8 and the tests::

    $ make flake8
    $ make test
   
8. If you have other Python versions installed, use the `tox` tool to test `python-TSIP` against them, too. You may have to 
   adjust ``tox.ini`` to match your environment but please don't ``git add tox.ini``.

    $ make tox
    
   To get flake8 and tox, just pip install them into your virtualenv. You may have to adjust your ``PATH`` before running
   ``make tox`` so that the respective Python interpreters are found. In my setup I the different Python versions are
   installed under ``/opt/Python-<version``::
   
    $ export PATH=$PATH:`echo /opt/Python-*/bin | tr ' ' ':'`

9. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin feature/<name-of-your-feature>

10. Submit a pull request through the GitHub website.

.. _gitflow: https://github.com/nvie/gitflow
.. _`A successful Git branching model`: http://nvie.com/posts/a-successful-git-branching-model/

Pull Request Guidelines
=======================

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy. Check
   https://travis-ci.org/mjuenema/python-TSIP/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
====

To run a subset of tests::

    $ nosetests tests/test_<name>.py
