# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sumo_tasks_pipeline',
 'sumo_tasks_pipeline.commons',
 'sumo_tasks_pipeline.file_handler',
 'sumo_tasks_pipeline.operation_module',
 'sumo_tasks_pipeline.pipeline']

package_data = \
{'': ['*']}

install_requires = \
['bs4', 'docker', 'google-cloud-storage', 'joblib', 'lxml', 'pandas']

extras_require = \
{'full': ['Shapely>=1.7.0,<2.0.0',
          'pyproj>=3.0.0,<4.0.0',
          'SumoNetVis>=1.6.0,<2.0.0',
          'geopandas>=0.10.0,<0.11.0',
          'geoviews>=1.9.1,<2.0.0']}

setup_kwargs = {
    'name': 'sumo-tasks-pipeline',
    'version': '4.0',
    'description': 'Simple Python interface for a traffic simulator: SUMO',
    'long_description': "# sumo-tasks-pipeline\n- - -\n\nRun SUMO simulators as easy as possible!\n\nThe package `sumo-tasks-pipeline` enables you to run a traffic simulator [SUMO](https://sumo.dlr.de/docs/index.html) efficiently \nand to interact with Python easily.\n\n# Example\n\nJust three lines to run a SUMO simulation.\n\n```python\nfrom sumo_tasks_pipeline import LocalSumoController, SumoConfigObject\nfrom pathlib import Path\n\npath_config = Path().cwd().joinpath('tests/resources/config_complete')\nsumo_controller = LocalSumoController(sumo_command='/usr/local/bin/sumo')\nsumo_config = SumoConfigObject(scenario_name='example', path_config_dir=path_config, config_name='grid.sumo.cfg')\nsumo_result_obj = sumo_controller.start_job(sumo_config)\n```\n\nSee `examples` directory to know more.\n\n# Features\n\n- Possible to resume your tasks. The feature is useful when you run simulators on Google Colab.\n- Possible to save SUMO simulation result to Google Cloud Storage (GCS). No worries even when your local storage is small.\n- Possible to run SUMO simulations with multiple machines if you use GCS as the storage backend.\n\n# Requirement\n\n- python > 3.5\n- docker \n- docker-compose\n\n# Install\n\n## Pull the image (or build of a docker image with SUMO)\n\nThe existing image is on the [Dockerhub](https://hub.docker.com/repository/docker/kensukemi/sumo-ubuntu18).\n\n```shell\ndocker pull kensukemi/sumo-ubuntu18\n```\n\nIf you prefer to build with yourself, you run the following command.\n\n```shell\ndocker-compose build \n```\n\n## Install a python package\n\n```shell\nmake install\n```\n\n\n# For developer\n\n```shell\npytest tests\n```\n\n# license and credit\n\nThe source code is licensed MIT. The website content is licensed CC BY 4.0.\n\n\n```\n@misc{sumo-docker-pipeline,\n  author = {Kensuke Mitsuzawa},\n  title = {sumo-tasks-pipeline},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/Kensuke-Mitsuzawa/sumo_docker_pipeline}},\n}\n```",
    'author': 'Kensuke Mitsuzawa',
    'author_email': 'kensuke.mit@gmail.com',
    'maintainer': 'Kensuke Mitsuzawa',
    'maintainer_email': 'kensuke.mit@gmail.com',
    'url': 'https://github.com/Kensuke-Mitsuzawa/sumo_docker_pipeline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
