# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyansys']

package_data = \
{'': ['*']}

install_requires = \
['ansys-dpf-core==0.6.0',
 'ansys-dpf-post==0.2.5',
 'ansys-fluent-core==0.11.0',
 'ansys-grantami-bomanalytics==1.0.1',
 'ansys-mapdl-core==0.63.2',
 'ansys-openapi-common==1.1.1',
 'ansys-platform-instancemanagement==1.0.2',
 'pyaedt==0.6.3']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.0,<5.0'],
 'all': ['ansys-mapdl-reader==0.52.0',
         'ansys-fluent-visualization==0.5.0',
         'ansys-fluent-parametric==0.5.0'],
 'docs': ['Sphinx==5.1.1', 'ansys-sphinx-theme==0.5.2'],
 'fluent-all': ['ansys-fluent-visualization==0.5.0',
                'ansys-fluent-parametric==0.5.0'],
 'mapdl-all': ['ansys-mapdl-reader==0.52.0']}

setup_kwargs = {
    'name': 'pyansys',
    'version': '2023.1.0',
    'description': 'Pythonic interfaces to Ansys products',
    'long_description': "PyAnsys metapackage\n===================\n|pyansys| |python| |pypi| |GH-CI| |MIT| |black|\n\n.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC\n   :target: https://docs.pyansys.com/\n   :alt: PyAnsys\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/pyansys?logo=pypi\n   :target: https://pypi.org/project/pyansys/\n   :alt: Python\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pyansys.svg?logo=python&logoColor=white\n   :target: https://pypi.org/project/pyansys/\n   :alt: PyPI\n\n.. |GH-CI| image:: https://github.com/pyansys/pyansys/actions/workflows/ci-build.yml/badge.svg\n   :target: https://github.com/pyansys/pyansys/actions/workflows/ci-build.yml\n   :alt: GH-CI\n\n.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat\n   :target: https://github.com/psf/black\n   :alt: Black\n\nWelcome to the PyAnsys metapackage repository. This project originated as a single ``pyansys`` package,\nwhich provides support to Ansys product releases. Compatibility of these packages amongst themselves\nand with the Ansys product release they are linked to is ensured.\n\nAt this moment, this package ensures the compatibility between the following PyAnsys packages:\n\n- `PyAEDT <https://aedt.docs.pyansys.com/>`_ : Pythonic interface to AEDT (Ansys Electronic Desktop)\n- `PyDPF-Core <https://dpf.docs.pyansys.com/>`_ : Pythonic interface to DPF (Data Processing Framework) for building more advanced and customized workflows\n- `PyDPF-Post <https://post.docs.pyansys.com/>`_ : Pythonic interface to DPF's postprocessing toolbox for manipulating and transforming simulation data\n- `PyFluent <https://fluent.docs.pyansys.com/>`_ : Pythonic interface to Ansys Fluent\n- `PyFluent-Parametric <https://fluentparametric.docs.pyansys.com/>`_ : Pythonic interface to Ansys Fluent parametric workflows\n- `PyFluent-Visualization <https://fluentvisualization.docs.pyansys.com/>`_ : Pythonic interface to visualize Ansys Fluent simulations using Python\n- `PyMAPDL <https://mapdl.docs.pyansys.com/>`_ : Pythonic interface to MAPDL.\n- `PyMAPDL Reader <https://reader.docs.pyansys.com/>`_: Pythonic interface to read legacy MAPDL result files (MAPDL 14.5 and later)\n- `PyPIM <https://pypim.docs.pyansys.com/>`_: Pythonic interface to communicate with the PIM (Product Instance Management) API\n- `Granta MI BoM Analytics <https://grantami.docs.pyansys.com/>`_: Pythonic interface to Granta MI BoM Analytics services\n- `Shared Components <https://shared.docs.pyansys.com/>`_: Shared software components to enable package interoperability and minimize maintenance\n\nMuch effort is underway to continue expanding and developing packages in the\n`PyAnsys GitHub <https://github.com/pyansys/>`__ account. On the ``Issues`` page\nfor each package, you can post issues and request new features. You can also email\nquestions to `PyAnsys Support <mailto:pyansys.support@ansys.com>`_.\n\nBy default, the PyAnsys package installs these core modules:\n\n- `PyAEDT`_\n- `PyDPF-Core`_\n- `PyDPF-Post`_\n- `PyFluent`_\n- `PyMAPDL`_\n- `PyPIM`_\n- `Granta MI BoM Analytics`_\n- `Shared Components`_\n\nHowever, the ``pyansys`` package also contains certain extra targets, which can be installed upon request:\n\n- **mapdl-all**: this target installs the core packages and `PyMAPDL Reader`_.\n- **fluent-all**: this target installs the core packages and `PyFluent-Parametric`_ and `PyFluent-Visualization`_.\n- **all**: this target install all extra ``pyansys`` packages.\n\nPackage installation\n--------------------\n\nTwo installation modes are provided: user and offline.\n\nUser mode installation\n^^^^^^^^^^^^^^^^^^^^^^\n\nBefore installing ``pyansys`` in user mode, ensure that you have the latest\nversion of `pip <https://pypi.org/project/pip/>`_ with:\n\n.. code:: bash\n   \n    python -m pip install -U pip\n\nThen, install ``pyansys`` with:\n\n.. code:: bash\n\n   python -m pip install pyansys\n\nIf you are interested in **installing an extra target** such as ``fluent-all``:\n\n.. code:: bash\n\n   python -m pip install pyansys[fluent-all]\n\nIf you are interested in **installing a specific version** such as ``2023.1.0``:\n\n.. code:: bash\n\n   python -m pip install pyansys==2023.1.0\n\nOffline mode installation\n^^^^^^^^^^^^^^^^^^^^^^^^^\n\nIf you lack an internet connection on your installation machine, the recommended way of installing\nthe ``pyansys`` metapackage is downloading the wheelhouse archive from the\n`Releases Page <https://github.com/pyansys/pyansys/releases>`_ for your corresponding machine architecture.\n\nEach wheelhouse archive contains all the Python wheels necessary to install ``pyansys`` metapackage from\nscratch on Windows, Linux, and MacOS from Python 3.7 to 3.10. You can install this on an isolated system with\na fresh Python installation or on a virtual environment.\n\nFor example, on Linux with Python 3.7, unzip the wheelhouse archive and install it with the following:\n\n.. code:: bash\n\n    unzip pyansys-v2023.1.0-wheelhouse-Linux-3.7-core.zip wheelhouse\n    pip install pyansys -f wheelhouse --no-index --upgrade --ignore-installed\n\nIf you're on Windows with Python 3.9, unzip to a wheelhouse directory and install using the same command as above.\n\nConsider installing using a `virtual environment <https://docs.python.org/3/library/venv.html>`_.\n\nVersioning system\n-----------------\n\nThe ``pyansys`` metapackage follows a semantic-like versioning system, though it has been adapted to the\nAnsys product release mechanism. In that sense, the following kind of versioning system is followed:\n\n.. code:: bash\n\n   XXXX.Y.ZZ\n\nWhere:\n\n- ``XXXX`` is the Ansys product release year (for example, 2022)\n- ``Y`` is the Ansys product release within the same year (for example, 1, which relates to R1)\n- ``ZZ`` is the patched versions to the ``pyansys`` metapackage, if any.\n\nConsequently, the first ``pyansys`` metapackage compatible with the 2024 R2 release would be:\n\n.. code:: bash\n\n   2024.2.0\n\nAnd any subsequent patched version of that package would be:\n\n.. code:: bash\n\n   2024.2.1\n   2024.2.2\n   2024.2.3\n   ...\n\nYou can request for a specific version install when pip installing your package:\n\n.. code:: bash\n\n   python -m pip install pyansys==2024.2.0\n\nLicense and acknowledgments\n---------------------------\nAll PyAnsys libraries are licensed under the MIT license.\n\nPyAnsys libraries make no commercial claim over Ansys whatsoever. \nThese libraries extend the functionality of Ansys products by\nadding Python interfaces to legally obtained software products\nwithout changing the core behaviors or licenses of the original\nsoftware.  \n\nFor more information about Ansys products, visit the `Ansys web site <https://www.ansys.com/>`_.\n",
    'author': 'ANSYS, Inc.',
    'author_email': 'pyansys.support@ansys.com',
    'maintainer': 'PyAnsys developers',
    'maintainer_email': 'pyansys.maintainers@ansys.com',
    'url': 'https://github.com/pyansys',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
