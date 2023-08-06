# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photonbend',
 'photonbend.core',
 'photonbend.scripts',
 'photonbend.scripts.commands',
 'photonbend.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'click>=8.0.4,<9.0.0',
 'numpy>=1.22,<2.0',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['photonbend = photonbend.scripts.main:main']}

setup_kwargs = {
    'name': 'photonbend',
    'version': '1.0.0',
    'description': 'Photonbend allows one to convert photos between different sorts of lenses, rotate photos and make panoramas.',
    'long_description': "# Photonbend\nPhotonbend is a python module to handle photos, especially photos taken with fisheye lenses, and convert them between different kinds of lenses, FoV, and types of photos like inscribed circles, cropped circles, or even side-by-side double inscribed circles. It also allows you to rotate those photos, convert them to equirectangular panoramas or convert panoramas to fisheye photos.\n\nIt can be used as a library to handle images on your projects or it can be used as a standalone tool with its own set of commands to help you alter your photos taken with a [fisheye lens](https://en.wikipedia.org/wiki/Fisheye_lens), an [omnidirectional camera](https://en.wikipedia.org/wiki/Omnidirectional_(360-degree)_camera) such as the Samsung Gear 360 or an [equirectangular](https://en.wikipedia.org/wiki/Equirectangular_projection) panorama.\n\nIf you just want to use the tools go to the [Scripts](docs/scripts.md). If you want to undestand how it works just keep reading\n\n# Concepts\n## Fisheye photography\nUnlike rectilinear lenses, fisheye lenses can capture great angles like 180º and even greater. With the right setup we can nowadays produce 360º images.\n\n[![Equidistant Projection (lens)](docs/img/equidistant_small.jpg)](examples/equidistant.jpg)<br> ***A 360º fisheye photo with its center aiming at the ceiling.***[^1]\n\nThose type of images follow a scheme like the one below:\n\n![Inscribed image scheme](docs/img/fisheye-photo-scheme.png)</br>\n***Fisheye photo scheme depicting the angles produced by an equidistant lens***\n\n## How it works\n\nThis module uses the information you provide about the image format, lenses, and FoV, couples it with mathematical functions that describes the ways the lenses behave, and makes use of trigonometry to map your planar photos or panoramas to a sphere (actually, the interior wall of a sphere.\nUsing a sphere as a base lets you rotate the image. Using all those functions and trigonometry, it also lets you take a virtual picture of the interior of the sphere using different sorts of lenses and FoV to produce new images. It also lets you map a sphere to an equirectangular panorama.\n\n![Image maps](docs/img/mapping-comparison.png)\n\nYou can see examples on the [scripts page](docs/scripts.md)\n\n## Convention\nOn the case of the images this software was designed to handle, the convention we adopted was the the center of the image is the top of the sphere, and its borders are the maximum angle of the FoV (In case of a 360 degree image, the sphere's bottom). **This convention is important to understand the rotation scheme**.\n\n## Rotation\nThis tool lets you rotate your images. For reference, the rotation is defined in 3 degrees of freedom, namely: pitch, yaw and roll, and their direction of rotation are those shown in the image below:\n\n![Rotation](docs/img/Rotation.png)</br>\n***For reference, on the scheme above, we are visualizing the image sphere looking down from its top.***\n\n# Scripts\nThe module installs a a script 3 different commands to help you deal with your images.\n - [make-photo](docs/scripts.md#make-photo)\n - [alter-photo](docs/scripts.md#alter-photo)\n - [make-pano](docs/scripts.md#make-pano)\n\n[^1]:\n    ## About the source image used on the examples:\n\n    Author: Bob Dass <br>\n    Title: View From The Deck <br>\n    Available at: https://flickr.com/photos/54144402@N03/50677156243/in/faves-195024173@N05/ <br>\n    License: Creative Commons - Attribution 2.0 <br>\n    [License summary here](https://creativecommons.org/licenses/by/2.0/) <br>\n    [License text here](https://creativecommons.org/licenses/by/2.0/legalcode) <br>",
    'author': 'Edson Moreira',
    'author_email': 'w.moreirae@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
