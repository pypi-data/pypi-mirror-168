# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depdive']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.0,<9.0.0',
 'package-locator>=0.4.4,<0.5.0',
 'rich>=10.3.0,<11.0.0',
 'version-differ>=0.3.14,<0.4.0']

entry_points = \
{'console_scripts': ['depdive = depdive.__main__:main']}

setup_kwargs = {
    'name': 'depdive',
    'version': '0.0.42',
    'description': 'Performs security checks for a dependency update',
    'long_description': 'Depdive\n===========================\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/depdive.svg\n   :target: https://pypi.org/project/depdive/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/depdive\n   :target: https://pypi.org/project/depdive\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/nasifimtiazohi/depdive\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/depdive/latest.svg?label=Read%20the%20Docs\n   :target: https://depdive.readthedocs.io/\n   :alt: Read the documentation at https://depdive.readthedocs.io/\n.. |Build| image:: https://github.com/nasifimtiazohi/depdive/workflows/Build%20depdive%20Package/badge.svg\n   :target: https://github.com/nasifimtiazohi/depdive/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/nasifimtiazohi/depdive/workflows/Run%20depdive%20Tests/badge.svg\n   :target: https://github.com/nasifimtiazohi/depdive/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/nasifimtiazohi/depdive/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/nasifimtiazohi/depdive\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n   \n  \n\nEach time you accept a dependency update, you are pulling in new third-party code. However, how to ensure the update is secure? \n\nOne way to put a security (and quality) control check before accepting an update is to check what part of the code changes has passed through a code review process. Depdive automates this check.\n\n\nWorkflow\n--------\n\nDepdive maps code changes between two versions of a package uploaded in the registry to the corresponding commits that made these changes in the source repository. Depdive then identifies if there was a reviewer for the mapped commit(s) through rule-based checks for evidence of code review on GitHub.\n\nAlong the process, Depdive also outputs phantom artifacts: files and lines that are present in the registry but not present in the repository. Examples of phantom files can be compiled binaries in PyPI packages, transpiled JavaScript in npm, and other auto-generated files. Not to mention, malicious actors can sneak in code in the last mile between the repository and the registry. \n\nDepdive works for four package registries: (1) Crates.io (Rust), (2) npm (JavaScript), (3) PyPI (Python), and (4) RubyGems (Ruby).\nCurrently, Depdive only works for GitHub repositories, as GitHub is our primary source to check for code review. \n\n\n.. image:: docs/images/depdive.drawio.png\n\nFeatures\n--------\n\n* Outputs changes that have (and have not) been code reviewed in a dependency update. You can calculate the code review coverage from the output by dividing the reviewed lines by the total lines of code changes in an update.\n* Outputs the reviewed and non-reviewed commits. Also outputs how we determined if a commit was code-reviewed, and the actors involved in the review.\n* Outputs files present in the update version downloaded from the registry but not in the source repository, ie phantom files.\n* Outputs code changes that are present in the udpate, but cannot be mapped to changes in the repository, ie phantom lines.\n\n\nInstallation\n------------\n\nYou can install *depdive* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install depdive\n\n\nUsage\n-----\n.. code-block:: python\n\n    ca = CodeReviewAnalysis(CARGO, "tokio", "1.8.4", "1.9.0")\n    stats = ca.stats\n    assert stats.phantom_files == 0\n    assert stats.files_with_phantom_lines == 0\n    assert stats.phantom_lines == 0\n    assert stats.reviewed_lines == 3694\n    assert stats.non_reviewed_lines == 0\n    assert stats.total_commit_count == 29\n    assert stats.reviewed_commit_count == 29\n    \n    ca = CodeReviewAnalysis(RUBYGEMS, "pundit", "2.1.0", "2.1.1")\n    stats = ca.stats\n    assert stats.phantom_files == 0\n    assert stats.files_with_phantom_lines == 0\n    assert stats.phantom_lines == 0\n    assert stats.reviewed_lines == 128\n    assert stats.non_reviewed_lines == 186\n    assert stats.total_commit_count == 35\n    assert stats.reviewed_commit_count == 23\n    \n    ca = CodeReviewAnalysis(PYPI, "numpy", "1.21.4", "1.21.5")\n    stats = ca.stats\n    assert stats.phantom_files == 39\n    assert stats.files_with_phantom_lines == 1\n    assert stats.phantom_lines == 3\n    assert stats.reviewed_lines == 245\n    assert stats.non_reviewed_lines == 12\n    assert stats.total_commit_count == 10\n    assert stats.reviewed_commit_count == 9\n    \n    ca = CodeReviewAnalysis(NPM, "lodash", "4.17.20", "4.17.21")\n    stats = ca.stats\n    assert stats.phantom_files == 1046\n    assert stats.files_with_phantom_lines == 1\n    assert stats.phantom_lines == 1\n    assert stats.reviewed_lines == 58\n    assert stats.non_reviewed_lines == 14\n    assert stats.total_commit_count == 3\n    assert stats.reviewed_commit_count == 2\n    \n\nFuture Work\n------------\n\n* Also provide the quality of the code review(s), e.g., what is the relation between the author and the reviewer? Was a sock account used to bypass the code review check?\n* What other checks should we perform for an update?\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://depdive.readthedocs.io/en/latest/usage.html\n',
    'author': 'Nasif Imtiaz',
    'author_email': 'nasifimtiaz88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nasifimtiazohi/depdive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
