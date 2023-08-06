# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agora',
 'agora.io',
 'agora.utils',
 'aliby',
 'aliby.io',
 'aliby.tile',
 'aliby.utils',
 'extraction',
 'extraction.core',
 'extraction.core.functions',
 'extraction.core.functions.custom',
 'extraction.examples',
 'logfile_parser',
 'postprocessor',
 'postprocessor.benchmarks',
 'postprocessor.core',
 'postprocessor.core.functions',
 'postprocessor.core.multisignal',
 'postprocessor.core.processes',
 'postprocessor.routines']

package_data = \
{'': ['*'],
 'extraction.examples': ['pairs_data/*'],
 'logfile_parser': ['grammars/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aliby-baby>=0.1.14,<0.2.0',
 'dask>=2021.12.0,<2022.0.0',
 'flatten-dict>=0.4.2,<0.5.0',
 'gaussianprocessderivatives>=0.1.5,<0.2.0',
 'h5py==2.10',
 'imageio==2.8.0',
 'leidenalg>=0.8.8,<0.9.0',
 'more-itertools>=8.12.0,<9.0.0',
 'numpy>=1.21.6',
 'opencv-python==4.1.2.30',
 'p-tqdm>=1.3.3,<2.0.0',
 'pandas>=1.3.3',
 'pathos>=0.2.8,<0.3.0',
 'py-find-1st>=1.1.5,<2.0.0',
 'pycatch22>=0.4.2,<0.5.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'scikit-image>=0.18.1',
 'scikit-learn>=1.0.2',
 'scipy>=1.7.3',
 'tqdm>=4.62.3,<5.0.0',
 'xmltodict>=0.13.0,<0.14.0']

extras_require = \
{'network': ['omero-py>=5.6.2', 'zeroc-ice==3.6.5'],
 'omero': ['omero-py>=5.6.2']}

setup_kwargs = {
    'name': 'aliby',
    'version': '0.1.43',
    'description': 'Process and analyse live-cell imaging data',
    'long_description': '# ALIBY (Analyser of Live-cell Imaging for Budding Yeast)\n\n[![docs](https://readthedocs.org/projects/aliby/badge/?version=latest)](https://aliby.readthedocs.io/en/latest)\n[![PyPI version](https://badge.fury.io/py/aliby.svg)](https://badge.fury.io/py/aliby)\n[![pipeline](https://git.ecdf.ed.ac.uk/swain-lab/aliby/aliby/badges/master/pipeline.svg?key_text=master)](https://git.ecdf.ed.ac.uk/swain-lab/aliby/aliby/-/pipelines)\n[![dev pipeline](https://git.ecdf.ed.ac.uk/swain-lab/aliby/aliby/badges/dev/pipeline.svg?key_text=dev)](https://git.ecdf.ed.ac.uk/swain-lab/aliby/aliby/-/commits/dev)\n\nEnd-to-end processing of cell microscopy time-lapses. ALIBY automates segmentation, tracking, lineage predictions, post-processing and report production. It leverages the existing Python ecosystem and open-source scientific software available to produce seamless and standardised pipelines.\n\n## Quickstart Documentation\n\nWe use (and recommend) [OMERO](https://www.openmicroscopy.org/omero/) to manage our microscopy database, but ALIBY can process both locally-stored experiments and remote ones hosted on a server.\n\n### Setting up a server\nFor testing and development, the easiest way to set up an OMERO server is by\nusing Docker images.\n[The software carpentry](https://software-carpentry.org/) and the [Open\n Microscopy Environment](https://www.openmicroscopy.org), have provided\n[instructions](https://ome.github.io/training-docker/) to do this.\n\nThe `docker-compose.yml` file can be used to create an OMERO server with an\naccompanying PostgreSQL database, and an OMERO web server.\nIt is described in detail\n[here](https://ome.github.io/training-docker/12-dockercompose/).\n\nOur version of the `docker-compose.yml` has been adapted from the above to\nuse version 5.6 of OMERO.\n\nTo start these containers (in background):\n```shell script\ncd pipeline-core\ndocker-compose up -d\n```\nOmit the `-d` to run in foreground.\n\nTo stop them, in the same directory, run:\n```shell script\ndocker-compose stop\n```\n\n### Installation\n\nSee our [installation instructions]( https://aliby.readthedocs.io/en/latest/INSTALL.html ) for more details.\n\n### Raw data access\n\n ```python\nfrom aliby.io.dataset import Dataset\nfrom aliby.io.image import Image\n\nserver_info= {\n            "host": "host_address",\n            "username": "user",\n            "password": "xxxxxx"}\nexpt_id = XXXX\ntps = [0, 1] # Subset of positions to get.\n\nwith Dataset(expt_id, **server_info) as conn:\n    image_ids = conn.get_images()\n\n#To get the first position\nwith Image(list(image_ids.values())[0], **server_info) as image:\n    dimg = image.data\n    imgs = dimg[tps, image.metadata["channels"].index("Brightfield"), 2, ...].compute()\n    # tps timepoints, Brightfield channel, z=2, all x,y\n```\n\n### Tiling the raw data\n\nA `Tiler` object performs trap registration. It may be built in different ways but the simplest one is using an image and a the default parameters set.\n\n```python\nfrom aliby.tile.tiler import Tiler, TilerParameters\nwith Image(list(image_ids.values())[0], **server_info) as image:\n    tiler = Tiler.from_image(image, TilerParameters.default())\n    tiler.run_tp(0)\n```\n\nThe initialisation should take a few seconds, as it needs to align the images\nin time.\n\nIt fetches the metadata from the Image object, and uses the TilerParameters values (all Processes in aliby depend on an associated Parameters class, which is in essence a dictionary turned into a class.)\n\n#### Get a timelapse for a given trap\n```python\nfpath = "h5/location"\n\ntrap_id = 9\ntrange = list(range(0, 30))\nncols = 8\n\nriv = remoteImageViewer(fpath)\ntrap_tps = riv.get_trap_timepoints(trap_id, trange, ncols)\n```\n\nThis can take several seconds at the moment.\nFor a speed-up: take fewer z-positions if you can.\n\nIf you\'re not sure what indices to use:\n```python\nseg_expt.channels # Get a list of channels\nchannel = \'Brightfield\'\nch_id = seg_expt.get_channel_index(channel)\n\nn_traps = seg_expt.n_traps # Get the number of traps\n```\n\n#### Get the traps for a given time point\nAlternatively, if you want to get all the traps at a given timepoint:\n\n```python\ntimepoint = 0\nseg_expt.get_tiles_timepoints(timepoint, tile_size=96, channels=None,\n                                z=[0,1,2,3,4])\n```\n\n\n### Contributing\nSee [CONTRIBUTING.md](./CONTRIBUTING.md) for installation instructions.\n',
    'author': 'Alan Munoz',
    'author_email': 'alan.munoz@ed.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
