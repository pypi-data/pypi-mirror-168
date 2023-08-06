# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybuoy', 'pybuoy.api', 'pybuoy.mixins', 'pybuoy.observation']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pybuoy',
    'version': '0.4.3',
    'description': 'Python wrapper for NDBC data.',
    'long_description': "pybuoy - Python NDBC API Wrapper\n================================\n\n.. image:: https://img.shields.io/pypi/v/pybuoy?color=blue\n    :alt: Latest Version\n    :target: https://pypi.python.org/pypi/pybuoy\n\n.. image:: https://img.shields.io/pypi/pyversions/pybuoy\n    :alt: Supported Python Versions\n    :target: https://pypi.python.org/pypi/pybuoy\n\n.. image:: https://img.shields.io/pypi/dm/pybuoy\n    :alt: PyPI - Monthly Downloads\n    :target: https://pypi.python.org/pypi/pybuoy\n\n\n``pybuoy`` is a server-side Python package that was built to facilitate rapid discovery of new data from `NDBC <https://www.ndbc.noaa.gov>`_ with only a single dependency!\n\nInstallation\n------------\n\n``pybuoy`` is supported on Python 3.10+ and can be installed with either pip or a package manager like `poetry <https://python-poetry.org>`_:\n\n- **with pip**: ``pip install pybuoy``\n\n  - recommended to install any third party library in `python's virtualenv <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments>`_.\n\n- **with poetry**: ``poetry add pybuoy``\n\n  - automatically creates and manages `python's virtualenvs <https://realpython.com/dependency-management-python-poetry>`_.\n\nQuickstart\n----------\n\n.. code-block:: python\n\n    from pybuoy import Buoy\n\n    buoy = Buoy()\n\n\nWith the ``buoy`` instance you can then interact with NDBC:\n\n- `Get all active stations <https://pybuoy.readthedocs.io/en/latest/tutorials/active_buoys.html>`_.\n\n- `Get realtime meteorological data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-meteorological-data>`_ for buoy by station_id.\n\n- `Get realtime wave summary data <https://pybuoy.readthedocs.io/en/latest/tutorials/realtime_data.html#get-wave-summary-data>`_ for buoy by station_id.\n",
    'author': 'Kyle J. Burda',
    'author_email': 'kylejbdev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
