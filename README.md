Installation
============

[![Python package](https://img.shields.io/github/actions/workflow/status/chdemko/pandoc-glfm/python-package.yml?logo=github&branch=develop)](https://github.com/chdemko/pandoc-glfm/actions/workflows/python-package.yml)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Coveralls](https://img.shields.io/coveralls/github/chdemko/pandoc-glfm/develop.svg?logo=Codecov&logoColor=white)](https://coveralls.io/github/chdemko/pandoc-glfm?branch=develop)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/chdemko/pandoc-glfm.svg?logo=scrutinizer)](https://scrutinizer-ci.com/g/chdemko/pandoc-glfm/)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/chdemko/pandoc-glfm/develop.svg?logo=codefactor)](https://www.codefactor.io/repository/github/chdemko/pandoc-glfm)
[![Codacy](https://img.shields.io/codacy/grade/443f4a26698a4ba0be5064fe9323f2a0.svg?logo=codacy)](https://app.codacy.com/gh/chdemko/pandoc-glfm/dashboard)
[![PyPI version](https://img.shields.io/pypi/v/pandoc-glfm.svg?logo=pypi&logoColor=white)](https://pypi.org/project/pandoc-glfm/)
[![PyPI format](https://img.shields.io/pypi/format/pandoc-glfm.svg?logo=pypi&logoColor=white)](https://pypi.org/project/pandoc-glfm/)
[![License](https://img.shields.io/pypi/l/pandoc-glfm.svg?logo=pypi&logoColor=white)](https://raw.githubusercontent.com/chdemko/pandoc-glfm/develop/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/pandoc-glfm?logo=pypi&logoColor=white)](https://pepy.tech/project/pandoc-glfm)
[![Development Status](https://img.shields.io/pypi/status/pandoc-glfm.svg?llogo=pypi&logoColor=white)](https://pypi.org/project/pandoc-glfm/)
[![Python version](https://img.shields.io/pypi/pyversions/pandoc-glfm.svg?logo=Python&logoColor=white)](https://pypi.org/project/pandoc-glfm/)
[![Pandoc version](https://img.shields.io/badge/pandoc-3.1%20..%203.7-blue.svg?logo=markdown)](https://pandoc.org/)
[![Latest release](https://img.shields.io/github/release-date/chdemko/pandoc-glfm.svg?logo=github)](https://github.com/chdemko/pandoc-glfm/releases)
[![Last commit](https://img.shields.io/github/last-commit/chdemko/pandoc-glfm/develop?logo=github)](https://github.com/chdemko/pandoc-glfm/commit/develop/)
[![Repo Size](https://img.shields.io/github/repo-size/chdemko/pandoc-glfm.svg?logo=github)](http://pandoc-glfm.readthedocs.io/en/latest/)
[![Code Size](https://img.shields.io/github/languages/code-size/chdemko/pandoc-glfm.svg?logo=github)](http://pandoc-glfm.readthedocs.io/en/latest/)
[![Source Rank](https://img.shields.io/librariesio/sourcerank/pypi/pandoc-glfm.svg?logo=libraries.io&logoColor=white)](https://libraries.io/pypi/pandoc-glfm)
[![Docs](https://img.shields.io/readthedocs/pandoc-glfm.svg?logo=read-the-docs&logoColor=white)](http://pandoc-glfm.readthedocs.io/en/latest/)

*pandoc-glfm* is a [pandoc] filter for adding some **G**it**L**ab **F**lavored
**M**arkdown features to pandoc:

* tip (note, tip, important, caution, warning) with title
  ~~~markdown
  > [!tip] My title
  > My tip
  ~~~
* task lists (with disabled tasks)
  ~~~markdown
  * [x] Finished task
  * [ ] To do task
  * [~] Disabled task
  ~~~
* tables using the `<br>` line separator
  ~~~markdown
  | Name | Details |
  | ---  | ---     |
  | Item1 | This text is on one line |
  | Item2 | This item has:<br><br>- Multiple items<br>- That we want listed separately |
  ~~~

[pandoc]: http://pandoc.org/

Instructions
------------

*pandoc-glfm* requires [python], a programming language that
comes pre-installed on linux and Mac OS X, and which is easily installed
[on Windows].

Install *pandoc-glfm* using the bash command

~~~shell-session
$ pipx install pandoc-glfm
~~~

To upgrade to the most recent release, use

~~~shell-session
$ pipx upgrade pandoc-glfm
~~~

`pipx` is a script to install and run python applications in isolated
environments from the Python Package Index, [PyPI]. It can be installed
using instructions given [here](https://pipx.pypa.io/stable/).

[python]: https://www.python.org
[on Windows]: https://www.python.org/downloads/windows
[PyPI]: https://pypi.org


Getting Help
------------

If you have any difficulties with pandoc-glfm, please feel
welcome to [file an issue] on github so that we can help.

[file an issue]: https://github.com/chdemko/pandoc-glfm/issues

Contribute
==========

Instructions
------------

Install `hatch`, then run

~~~shell-session
$ hatch run pip install pre-commit
$ hatch run pre-commit install
~~~

to install `pre-commit` before working on your changes.

Tests
-----

When your changes are ready, run

~~~shell-session
$ hatch test
$ hatch fmt --check
$ hatch run lint:check
$ hatch run docs:build
$ hatch build -t wheel
~~~

for running the tests, checking the style, building the documentation
and building the wheel.

