# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal',
 'fractal.client',
 'fractal.client.cmd',
 'fractal.common',
 'fractal.common.models']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pydantic>=1.10.1,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rich>=12.5.1,<13.0.0',
 'sqlmodel>=0.0.8,<0.0.9']

entry_points = \
{'console_scripts': ['fractal = fractal.__main__:run',
                     'fractal_new = fractal.new:run',
                     'fractal_old = fractal.old:run']}

setup_kwargs = {
    'name': 'fractal-client',
    'version': '0.2.1',
    'description': 'Client and common components of the Fractal analytics platform',
    'long_description': "# Fractal Client\n\n[![PyPI version](https://img.shields.io/pypi/v/fractal-client?color=gree)](https://pypi.org/project/fractal-client/)\n\nFractal is a framework to process high content imaging data at scale and prepare it for interactive visualization.\n\nFractal provides distributed workflows that convert TBs of image data into OME-Zarr files. The platform then processes the 3D image data by applying tasks like illumination correction, maximum intensity projection, 3D segmentation using [cellpose](https://cellpose.readthedocs.io/en/latest/) and measurements using [napari workflows](https://github.com/haesleinhuepf/napari-workflows). The pyramidal OME-Zarr files enable interactive visualization in the napari viewer.\n\n![Fractal_Overview](https://user-images.githubusercontent.com/18033446/190978261-2e7b57e9-72c7-443e-9202-15d233f8416d.jpg)\n\n\nThis is the main Fractal repository that contains the **Fractal client** and some examples. The **Fractal core tasks** to parse images and process OME-Zarr files can be found [here](https://github.com/fractal-analytics-platform/fractal-tasks-core). The **Fractal server** can be found [here](https://github.com/fractal-analytics-platform/fractal-server).\n\nExample input data for Fractal can be found here: [10.5281/zenodo.7057076](https://doi.org/10.5281/zenodo.7057076)\nExample output data from Fractal in the OME-Zarr format can be found here: [10.5281/zenodo.7081622](https://doi.org/10.5281/zenodo.7081622)\nExample workflows can be found in the `examples` folder, together with additional instructions for how to set up the server & client, download the test data and run workflows through Fractal.\n\nFractal is currently in an early alpha version. We have the core processing functionality working for Yokogawa CV7000 image data and a workflow for processing OME-Zarr images up to feature measurements. But we're still adding core functionality and will introduce breaking changes. You can follow along our planned milestones on the [architecture side](https://github.com/fractal-analytics-platform/fractal/milestones) & the [tasks side](https://github.com/fractal-analytics-platform/fractal-tasks-core). Open an issue to get in touch, raise bugs or ask questions.\n\nOME-Zarr files can be interactively visualizated in napari. Here is an example using the newly-proposed async loading in [NAP4](https://github.com/napari/napari/pull/4905) and the [napari-ome-zarr plugin](https://github.com/ome/napari-ome-zarr):\n\n![napari_plate_overview](https://user-images.githubusercontent.com/18033446/190983839-afb9743f-530c-4b00-bde7-23ad62404ee8.gif)\n\n### Contributors\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute for Biomedical Research and in the Pelkmans Lab at the University of Zurich (both in Switzerland). The project lead is with [@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi).\nThe core development is done under contract by [@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa) & [jacopo-exact](https://github.com/jacopo-exact) from eXact lab S.r.l. <exact-lab.it>.\n\n## Installation\n\nSimply\n\n``` pip install fractal-client ```\n\nSubsequently, you may invoke it as `fractal`. Note that you must provide\nthe following environment variables:\n\n* `FRACTAL_SERVER`: fully qualified URL to the Fractal server installation\n* `FRACTAL_USER`, `FRACTAL_PASSWORD`: email and password used to log-in to the\n   Fractal server\n\nBy default, `fractal` caches some information in `~/.fractal`. This destination\ncan be customized by setting `SESSION_CACHE_PATH`.\n\nFor ease of use, you may define an environment file `.fractal.env` in the\nfolder from which `fractal` is invoked.\n\n\n## Development\n\nDevelopment takes place on Github. You are welcome to submit an issue and open\npull requests.\n\n### Developmente installation\n\nFractal is developed and maintained using [poetry](https://python-poetry.org/).\n\nAfter cloning the repo, use\n\n```\npoetry install --with dev\n```\n\nto set up the development environment and all the dependencies and\ndev-dependencies. You may run the test suite with\n\n```\npoetry run pytest\n```\n\n### Releasing\n\nBefore release checklist:\n\n- [ ] The `main` branch is checked out\n- [ ] You reviewed dependencies and dev dependencies and the lock file is up to\n      date with `pyproject.toml`.\n- [ ] The current `HEAD` of the main branch passes all the tests\n- [ ] Use\n```\npoetry run bumpver update --dry --[patch|minor] --tag-commit --commit\n```\nto test updating the version bump\n- [ ] If the previous step looks good, use\n```\npoetry run bumpver update --[patch|minor] --tag-commit --commit\n```\nto actually bump the version and commit the changes locally.\n- [ ] Test the build with\n```\npoetry build\n```\n- [ ] If the previous step was successful, push the version bump and tags:\n```\ngit push && git push --tags\n```\n- [ ] Finally, publish the updated package to pypi with\n```\npoetry publish --dry-run\n```\nremoving the `--dry-run` when you made sure that everything looks good.\n",
    'author': 'Jacopo Nespolo',
    'author_email': 'jacopo.nespolo@exact-lab.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fractal-analytics-platform/fractal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
