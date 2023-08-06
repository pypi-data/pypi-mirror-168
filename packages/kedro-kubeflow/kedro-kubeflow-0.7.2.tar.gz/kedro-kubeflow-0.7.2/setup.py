# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kedro_kubeflow', 'kedro_kubeflow.generators']

package_data = \
{'': ['*'], 'kedro_kubeflow': ['templates/*']}

install_requires = \
['click>=8.0.4',
 'fsspec>=2021.4,<=2022.1',
 'kedro>=0.18.1,<0.19.0',
 'kfp>=1.8.12,<2.0',
 'semver>=2.10,<3.0',
 'tabulate>=0.8.7']

extras_require = \
{'gcp': ['google-auth<3', 'gcsfs>=2021.4,<=2022.1'],
 'mlflow': ['kedro-mlflow>=0.11.1,<0.12.0']}

entry_points = \
{'kedro.hooks': ['kubeflow_mlflow_tags_hook = '
                 'kedro_kubeflow.hooks:mlflow_tags_hook'],
 'kedro.project_commands': ['kubeflow = kedro_kubeflow.cli:commands']}

setup_kwargs = {
    'name': 'kedro-kubeflow',
    'version': '0.7.2',
    'description': 'Kedro plugin with Kubeflow Pipelines support',
    'long_description': '# Kedro Kubeflow Plugin\n\n[![Python Version](https://img.shields.io/pypi/pyversions/kedro-kubeflow)](https://github.com/getindata/kedro-kubeflow)\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![SemVer](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)\n[![PyPI version](https://badge.fury.io/py/kedro-kubeflow.svg)](https://pypi.org/project/kedro-kubeflow/)\n[![Downloads](https://pepy.tech/badge/kedro-kubeflow)](https://pepy.tech/project/kedro-kubeflow)\n\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-kubeflow&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-kubeflow)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=getindata_kedro-kubeflow&metric=coverage)](https://sonarcloud.io/summary/new_code?id=getindata_kedro-kubeflow)\n[![Documentation Status](https://readthedocs.org/projects/kedro-kubeflow/badge/?version=latest)](https://kedro-kubeflow.readthedocs.io/en/latest/?badge=latest)\n\n## About\n\nThe main purpose of this plugin is to enable running kedro pipeline on Kubeflow Pipelines. It supports translation from \nKedro pipeline DSL to [kfp](https://www.kubeflow.org/docs/pipelines/sdk/sdk-overview/) (pipelines SDK) and deployment to \na running kubeflow cluster with some convenient commands.\n\nThe plugin can be used together with `kedro-docker` to simplify preparation of docker image for pipeline execution.   \n\n## Documentation\n\nFor detailed documentation refer to https://kedro-kubeflow.readthedocs.io/\n\n## Usage guide\n\n\n```\nUsage: kedro kubeflow [OPTIONS] COMMAND [ARGS]...\n \n   Interact with Kubeflow Pipelines\n \n Options:\n   -h, --help  Show this message and exit.\n \n Commands:\n   compile          Translates Kedro pipeline into YAML file with Kubeflow pipeline definition\n   init             Initializes configuration for the plugin\n   list-pipelines   List deployed pipeline definitions\n   run-once         Deploy pipeline as a single run within given experiment.\n   schedule         Schedules recurring execution of latest version of the pipeline\n   ui               Open Kubeflow Pipelines UI in new browser tab\n   upload-pipeline  Uploads pipeline to Kubeflow server\n```\n\n## Configuration file\n\n`kedro init` generates configuration file for the plugin, but users may want\nto adjust it to match the run environment requirements: https://kedro-kubeflow.readthedocs.io/en/latest/source/02_installation/02_configuration.html\n\n',
    'author': 'Mateusz Pytel',
    'author_email': 'mateusz.pytel@getindata.com',
    'maintainer': 'GetInData MLOPS',
    'maintainer_email': 'mlops@getindata.com',
    'url': 'https://github.com/getindata/kedro-kubeflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
