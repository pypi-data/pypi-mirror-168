# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractal_tasks_core']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5-Qt5>=5.15.2,<6.0.0',
 'PyQt5-sip>=12.11.0,<13.0.0',
 'PyQt5>=5.15.7,<6.0.0',
 'anndata>=0.8.0,<0.9.0',
 'cellpose==2',
 'dask>=2022.6,<2022.8',
 'defusedxml>=0.7.1,<0.8.0',
 'graphviz>=0.20,<0.21',
 'imagecodecs>=2022.2.22,<2023.0.0',
 'llvmlite>=0.39.1,<0.40.0',
 'napari-skimage-regionprops>=0.5.3,<0.6.0',
 'napari-workflows>=0.2.3,<0.3.0',
 'ome-zarr>=0.5.1,<0.6.0',
 'pandas>=1.2.0,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0']

setup_kwargs = {
    'name': 'fractal-tasks-core',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Fractal Core Tasks\n\n[![PyPI version](https://img.shields.io/pypi/v/fractal-tasks-core?color=gree)](https://pypi.org/project/fractal-tasks-core/)\n\nFractal is a framework to process high content imaging data at scale and prepare it for interactive visualization.\n\nFractal provides distributed workflows that convert TBs of image data into OME-Zarr files. The platform then processes the 3D image data by applying tasks like illumination correction, maximum intensity projection, 3D segmentation using [cellpose](https://cellpose.readthedocs.io/en/latest/) and measurements using [napari workflows](https://github.com/haesleinhuepf/napari-workflows). The pyramidal OME-Zarr files enable interactive visualization in the napari viewer.\n\n![Fractal_Overview](https://user-images.githubusercontent.com/18033446/190978261-2e7b57e9-72c7-443e-9202-15d233f8416d.jpg)\n\nThis is the tasks repository, containing the python tasks that parse Yokogawa CV7000 images into OME-Zarr and process OME-Zarr files. Find more information about Fractal in general and the other repositories at the [main repository here](https://github.com/fractal-analytics-platform/fractal).\n\nAll tasks are written as python functions and are optimized for usage in Fractal workflows. But they can also be used as standalone functions to parse data or process OME-Zarr files. We heavily use regions of interest (ROIs) in our OME-Zarr files to store the positions of field of views. ROIs are saved as AnnData tables following [this spec proposal](https://github.com/ome/ngff/pull/64). We save wells as large Zarr arrays instead of a collection of arrays for each field of view ([see details here](https://github.com/ome/ngff/pull/137)).\n\nHere is an example of the interactive visualization in napari using the newly-proposed async loading in [NAP4](https://github.com/napari/napari/pull/4905) and the [napari-ome-zarr plugin](https://github.com/ome/napari-ome-zarr):\n\n![napari_plate_overview](https://user-images.githubusercontent.com/18033446/190983839-afb9743f-530c-4b00-bde7-23ad62404ee8.gif)\n\n\n## Installation instructions\n\nTBD\n\n## Available tasks\n\nCurrently, the following tasks are available:\n- Create Zarr Structure: Task to generate the zarr structure based on Yokogawa metadata files\n- Yokogawa to Zarr: Parses the Yokogawa CV7000 image data and saves it to the Zarr file\n- Illumination Correction: Applies an illumination correction based on a flatfield image & subtracts a background from the image.\n- Image Labeling (& Image Labeling Whole Well): Applies a cellpose network to the image of a single ROI or the whole well. cellpose parameters can be tuned for optimal performance.\n- Maximum Intensity Projection: Creates a maximum intensity projection of the whole plate.\n- Measurement: Make some standard measurements (intensity & morphology) using napari workflows, saving results to AnnData tables.\n\nSome additional tasks are currently being worked on and some older tasks are still present in the fractal_tasks_core folder.\n\n## Contributors\n\nFractal was conceived in the Liberali Lab at the Friedrich Miescher Institute\nfor Biomedical Research and in the Pelkmans Lab at the University of Zurich\n(both in Switzerland). The project lead is with\n[@gusqgm](https://github.com/gusqgm) & [@jluethi](https://github.com/jluethi).\nThe core development is done under contract by\n[@mfranzon](https://github.com/mfranzon), [@tcompa](https://github.com/tcompa)\n& [@jacopo-exact](https://github.com/jacopo-exact) from [eXact lab\nS.r.l.](https://exact-lab.it).\n\n## License\n\nFractal is released according to a BSD 3-Clause License. See `LICENSE`.\n',
    'author': 'Jacopo Nespolo',
    'author_email': 'jacopo.nespolo@exact-lab.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fractal-analytics-platform/fractal-tasks-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
