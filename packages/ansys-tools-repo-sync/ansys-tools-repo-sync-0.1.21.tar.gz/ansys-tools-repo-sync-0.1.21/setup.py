# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansys', 'ansys.tools.repo_sync']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'importlib-metadata>=4.0,<5.0',
 'pre-commit>=2.15.0,<3.0.0',
 'pygithub==1.55']

extras_require = \
{'docs': ['Sphinx>=4.4,<6.0',
          'numpydoc>=1.2,<2.0',
          'pyansys_sphinx_theme>=0.2,<0.3',
          'sphinx-copybutton>=0.4,<0.6'],
 'style': ['codespell>=2.1,<3.0', 'flake8>=3.9,<4.0'],
 'test': ['pytest>=7.0,<8.0', 'pytest-cov>=3.0,<4.0']}

entry_points = \
{'console_scripts': ['repo-sync = ansys.tools.repo_sync._cli:synchronize']}

setup_kwargs = {
    'name': 'ansys-tools-repo-sync',
    'version': '0.1.21',
    'description': 'Synchronize the content of two different repositories.',
    'long_description': '*********************\nansys-tools-repo-sync\n*********************\n\nThe ``ansys-tools-repo-sync`` library is intended to synchronize the content\nof two different repositories.\n\nWhat does this library do?\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nFor instance, due to intellectual properties concerns, it might not be possible\nto expose publicly the entire content of a private repository.\nIts owner could decide to have a second repository, a public one.\nPart of the content for this public repo would come from the private repository.\n\n``ansys-tools-repo-sync`` allows you to do so by copying a folder and its content\nfrom one repo to the other.\nIn addition, it is possible to filter the type extension file authorized to be copied.\n\n.. image:: doc/images/repo_sync.png\n    :align: center\n\n\nHow to use it?\n~~~~~~~~~~~~~~\n\nA common usage for this tool consist to integrate it in one of your CI/CD pipeline or workflow.\nFirstly, the tool must be installed.\n\n.. code:: bash\n\n    pip install ansys-tools-repo-sync\n\n\nThen, it can be used in the considered workflow with the appropriate arguments.\n\nRun it as follows:\n\n.. code:: bash\n\n    repo-sync --manifest path_to_manifest_file --repository target-repository-name --token github_token --organization ansys --protos-path path_to_protos_directory --dry-run\n\n.. note::\n    The ``--dry-run`` flag can be set while establishing the entire\n    workflow for the first time. It helps preventing unnecessary commits\n    of sensitive data. It will print the content expected to be committed in the\n    public repository.\n\nIssues\n------\nTo post issues, questions, and code, go to `ansys-tools-repo-sync Issues\n<https://github.com/ansys/ansys-tools-repo-sync/issues>`_.\n\n\n\nLicense\n-------\n``ansys-tools-repo-sync`` is licensed under the MIT license.\n',
    'author': 'ANSYS, Inc.',
    'author_email': 'None',
    'maintainer': 'PyAnsys developers',
    'maintainer_email': 'pyansys.support@ansys.com',
    'url': 'https://github.com/ansys/ansys-tools-repo-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
