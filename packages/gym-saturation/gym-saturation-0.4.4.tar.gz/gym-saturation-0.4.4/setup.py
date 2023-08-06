# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_saturation', 'gym_saturation.envs', 'gym_saturation.logic_ops']

package_data = \
{'': ['*'],
 'gym_saturation': ['resources/TPTP-mock/Axioms/*',
                    'resources/TPTP-mock/Problems/SET/*',
                    'resources/TPTP-mock/Problems/TST/*',
                    'resources/vampire-mock']}

install_requires = \
['gym>=0.21.0,<0.24.0', 'orjson', 'pexpect', 'tptp-lark-parser']

extras_require = \
{':python_version < "3.9"': ['importlib_resources']}

setup_kwargs = {
    'name': 'gym-saturation',
    'version': '0.4.4',
    'description': 'An OpenAI Gym environment for saturation provers',
    'long_description': '..\n  Copyright 2021-2022 Boris Shminke\n\n  Licensed under the Apache License, Version 2.0 (the "License");\n  you may not use this file except in compliance with the License.\n  You may obtain a copy of the License at\n\n      https://www.apache.org/licenses/LICENSE-2.0\n\n  Unless required by applicable law or agreed to in writing, software\n  distributed under the License is distributed on an "AS IS" BASIS,\n  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n  See the License for the specific language governing permissions and\n  limitations under the License.\n\n|Binder|\\ |PyPI version|\\ |Anaconda|\\ |CircleCI|\\ |Documentation Status|\\ |codecov|\\ |JOSS|\n\ngym-saturation\n==============\n\n``gym-saturation`` is a collection of `OpenAI Gym\n<https://gym.openai.com/>`__ environments for reinforcement learning\n(RL) agents striving to prove theorems. Currently, only theorems\nwritten in `TPTP library <https://tptp.org>`__ formal language in\nclausal normal form (CNF) are supported. ``gym-saturation``\nimplements the ‘given clause’ algorithm (similar to one used in\n`Vampire <https://github.com/vprover/vampire>`__ and `E Prover\n<https://github.com/eprover/eprover>`__).\n\nThere are two environments in ``gym-saturation``: ``SaturationEnv``\nand ``VampireEnv``. ``SaturationEnv`` is a saturation prover written\nin Python and was inspired by `PyRes\n<https://github.com/eprover/PyRes>`__. ``VampireEnv`` is a Python\nwrapper around a recent ``vampire`` binary and can be used to guide\n``vampire`` using RL.\n\nIn contrast to monolithic architecture of a typical Automated Theorem\nProver (ATP), ``gym-saturation`` gives different agents opportunities\nto select clauses themselves and train from their experience.\nCombined with a particular agent, ``gym-saturation`` can work as an\nATP.\n\n``gym-saturation`` can be interesting for RL practitioners willing to\napply their experience to theorem proving without coding all the\nlogic-related stuff themselves. It also can be useful for automated\ndeduction researchers who want to create an RL-empowered ATP.\n\nHow to Install\n==============\n\n.. attention::\n   If you want to use ``VampireEnv`` you should have a ``vampire``\n   binary on your machine.\n\nThe best way to install this package is to use ``pip``:\n\n.. code:: sh\n\n   pip install gym-saturation\n\nAnother option is to use ``conda``:\n\n.. code:: sh\n\n   conda install -c conda-forge gym-saturation\n   \nOne can also run it in a Docker container (with a pre-packed\n``vampire`` binary):\n\n.. code:: sh\n\n   docker build -t gym-saturation https://github.com/inpefess/gym-saturation.git\n   docker run -it --rm -p 8888:8888 gym-saturation jupyter-lab --ip=0.0.0.0 --port=8888\n\nHow to use\n==========\n\n.. code:: python\n\n   import gym_saturation\n   import gym\n   import os\n\n   env = gym.make(\n       "GymSaturation-v0", problem_list=["..."]\n   )\n   observation = env.reset()\n   observation, reward, done, info = env.step(action)\n\nSee `the\nnotebook <https://github.com/inpefess/gym-saturation/blob/master/examples/example.ipynb>`__\nor run it in\n`Binder <https://mybinder.org/v2/gh/inpefess/gym-saturation/HEAD?labpath=example.ipynb>`__\nfor more information.\n\nHow to Contribute\n=================\n\n`Pull requests <https://github.com/inpefess/gym-saturation/pulls>`__ are\nwelcome. To start:\n\n.. code:: sh\n\n   git clone https://github.com/inpefess/gym-saturation\n   cd gym-saturation\n   # activate python virtual environment with Python 3.7+\n   pip install -U pip\n   pip install -U setuptools wheel poetry\n   poetry install\n   # recommended but not necessary\n   pre-commit install\n   # install vampire binary\n   wget https://github.com/vprover/vampire/releases/download/v4.7/vampire4.7.zip -O vampire.zip\n   unzip vampire.zip\n   # then use vampire_z3_rel_static_HEAD_6295 as an argument or put in $PATH\n\nAll the tests in this package are\n`doctests <https://docs.python.org/3/library/doctest.html>`__. One can\nrun them with the following command:\n\n.. code:: sh\n\n   pytest --doctest-modules gym-saturation\n\nTo check the code quality before creating a pull request, one might run\nthe script ``local-build.sh``. It locally does nearly the same as the CI\npipeline after the PR is created.\n\nReporting issues or problems with the software\n==============================================\n\nQuestions and bug reports are welcome on `the\ntracker <https://github.com/inpefess/gym-saturation/issues>`__.\n\nMore documentation\n==================\n\nMore documentation can be found\n`here <https://gym-saturation.readthedocs.io/en/latest>`__.\n\n.. |PyPI version| image:: https://badge.fury.io/py/gym-saturation.svg\n   :target: https://badge.fury.io/py/gym-saturation\n.. |CircleCI| image:: https://circleci.com/gh/inpefess/gym-saturation.svg?style=svg\n   :target: https://circleci.com/gh/inpefess/gym-saturation\n.. |Documentation Status| image:: https://readthedocs.org/projects/gym-saturation/badge/?version=latest\n   :target: https://gym-saturation.readthedocs.io/en/latest/?badge=latest\n.. |codecov| image:: https://codecov.io/gh/inpefess/gym-saturation/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/inpefess/gym-saturation\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/inpefess/gym-saturation/HEAD?labpath=example.ipynb\n.. |JOSS| image:: https://joss.theoj.org/papers/c4f36ec7331a0dde54d8c3808fbff9c3/status.svg\n   :target: https://joss.theoj.org/papers/c4f36ec7331a0dde54d8c3808fbff9c3\n.. |Anaconda| image:: https://anaconda.org/conda-forge/gym-saturation/badges/version.svg\n   :target: https://anaconda.org/conda-forge/gym-saturation\n',
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/gym-saturation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
