# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatorgrade', 'gatorgrade.generate', 'gatorgrade.input', 'gatorgrade.output']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'gatorgrader>=1.1.0,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['gatorgrade = gatorgrade.main:app']}

setup_kwargs = {
    'name': 'gatorgrade',
    'version': '0.3.1',
    'description': 'GatorGrade executes GatorGrader checks!',
    'long_description': '# GatorGrade: A Python Tool to Implement GatorGrader\n\nGatorGrade is a Python tool that executes GatorGrader, an automatic grading tool\nthat can be used to check assignments through user-created checks. GatorGrade is\nthe newer Python-based version of\n[GatorGradle](https://github.com/GatorEducator/gatorgradle/blob/master/README.md).\n\n## Installing GatorGrade\n\nGatorGrade requires Python 3.7 or later. To install GatorGrade, we recommend\nusing the [`pipx`](https://pypa.github.io/pipx/) Python application installer.\nOnce you have `pipx` installed, you can install GatorGrade by running\n`pipx install gatorgrade`.\n\n## Using GatorGrade\n\nTo use GatorGrade to run GatorGrader checks for an assignment, the assignment\nmust contain a `gatorgrade.yml` file that defines the GatorGrader checks.\nInstructors, for more information on configuring the `gatorgrade.yml` file, see\nthe [Configuring GatorGrader Checks](#configuring-gatorgrader-checks) section\nbelow.\n\nTo use GatorGrade to run GatorGrader checks, run the `gatorgrade` command within\nthe assignment. This command will produce output that shows the passing\n(:heavy_check_mark:) or failing status (:x:) of each GatorGrader check as well\nas the overall percentage of passing checks. The following is the output of\nrunning GatorGrade on the [GatorGrade Hello\nWorld](https://github.com/GatorEducator/gatorgrade-hello-world/tree/main)\nassignment.\n\n```console\nRunning set up commands...\nInstalling dependencies from lock file\n\nNo dependencies to install or update\nSetup complete!\nFinished!\n\n✔  Complete all TODOs\n✔  Call the say_hello function\n✔  Call the say_hello_color function\n✘  Complete all TODOs\n✘  Write at least 25 words in writing/reflection.md\n✔  Pass pylint\n✔  Have a total of 5 commits, 2 of which were created by you\n\n-~-  FAILURES  -~-\n\n✘  Complete all TODOs\n   → Found 3 fragment(s) in the reflection.md or the output\n✘  Write at least 25 words in writing/reflection.md\n   → Found 3 word(s) in total of file reflection.md\n\n        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n        ┃ Passed 5/7 (71%) of checks for gatorgrade-hello-world! ┃\n        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n```\n\n## Configuring GatorGrader Checks\n\nInstructors can configure GatorGrader checks for an assignment by creating a\n`gatorgrade.yml` file. In this file, you can configure GatorGrader checks to run\nwithin a file context (i.e. for a specific file; `MatchFileFragment` is an\nexample of a GatorGrader check that should be run within a file context) _or_ in\nthe global context (i.e. for the assignment in general; `CountCommits` is an\nexample of a GatorGrader check that should be run in the global context).\n\nTo configure GatorGrader checks to run within a file context, specify the path\nto the file as a key (or nested keys) before specifying the GatorGrader checks.\nFor each GatorGrader check, define a `description` to print in the\noutput, the name of the `check`, and any [`options` specific to the GatorGrader check](https://www.gatorgrader.org/ember).\n\n```yml\n- src:\n    - hello_world.py:\n        - description: Complete all TODOs\n          check: MatchFileFragment\n          options:\n            fragment: TODO\n            count: 0\n        - description: Define a print statement\n          check: MatchFileFragment\n          options:\n            fragment: print(\n            count: 1\n```\n\nTo configure GatorGrader checks to run in the global context, specify the\nGatorGrader checks at the top level of the `gatorgrade.yml` file (i.e. not\nnested within any path).\n\n```yml\n- description: Have a total of 8 commits, 5 of which were created by you\n  check: CountCommits\n  options:\n    count: 8\n```\n\n### Using GatorGrade to Generate A Boilerplate `gatorgrade.yml` File\n\nFor convenience, instructors can use GatorGrade to generate a boilerplate\n`gatorgrade.yml` file that contains files or folders given to the GatorGrade command.\n\nTo generate a `gatorgrade.yml` file, run `gatorgrade generate <TARGET_PATH_LIST>`,\nwhere `<TARGET_PATH_LIST>` is a list of relative paths to files or folders you\nwant to include in the `gatorgrade.yml` file. These paths must correspond to\nexisting files or folders in the current directory. Any given folders will be\nexpanded to the files they contain. Please note that files and folders that\nstart with `__` or `.` and empty folders will be automatically ignored.\n\n## Contributing to GatorGrade\n\nIf you would like to contribute to GatorGrade, please refer to the [GatorGrade\nWiki](https://github.com/GatorEducator/gatorgrade/wiki/Contributing-Guidelines)\nfor contributing guidelines.\n',
    'author': 'Michael Abraham',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
