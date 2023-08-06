# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_meshes',
 'manim_meshes.delaunay',
 'manim_meshes.models',
 'manim_meshes.models.data_models',
 'manim_meshes.models.manim_models']

package_data = \
{'': ['*'], 'manim_meshes': ['shaders/mesh/*']}

install_requires = \
['ManimPango>=0.4.1,<0.5.0',
 'decorator>=5.0.9,<6.0.0',
 'manim>=0.15.2,<0.17.0',
 'manimgl>=1.6.1,<2.0.0',
 'numpy',
 'trimesh>=3.12.5,<4.0.0']

entry_points = \
{'manim.plugins': ['manim_meshes = module:object.attr']}

setup_kwargs = {
    'name': 'manim-meshes',
    'version': '0.0.5',
    'description': '2D and 3D Meshes for manim for displaying and educational Purposes.',
    'long_description': '[![Python Test and Lint](https://github.com/bmmtstb/manim-meshes/actions/workflows/python_ci_test.yaml/badge.svg)](https://github.com/bmmtstb/manim-meshes/actions/workflows/python_ci_test.yaml)\n# Manim for Meshes\n\n> ⚠️ Work in progress\n> \n> Most of the code will be rearranged or changed to use OpenGL, but OpenGL is not yet used throughout manim-ce. Stay tuned or feel free to assist.\n\nManim-Trimeshes implements manim functionalities for different types of meshes using either basic node-face data structures or by importing meshes from the python [trimesh](https://pypi.org/project/trimesh/ "trimesh on pypi") library.\n\nIt is mainly developed as a Project for Interactive Graphics Systems Group (GRIS) at TU Darmstadt, but is publicly available for everyone interested in rendering and animating meshes.\n\n## Installation\n\nManim-meshes has been published to [pypi](https://pypi.org/project/manim-meshes/) and therefore can be easily installed using:\n\n``pip install manim-meshes``\n\n## Usage\n\nKeep in mind this is a WIP...\n\n\n``from manim_meshes import *``\n\nThe basic `ManimMesh` and `Manim2DMesh` from `manim_models/basic_mesh` can currently only be used for smaller meshes (<1k Nodes), because it is dependent on the manim internal shaders which are not really implemented optimally. This type of mesh can be easily used for 2D and smaller 3D explanatory videos, not for high resolution rendering.\nThe more advanced `FastManimMesh` from `opengl_mesh` uses a custom shader which needs to be inserted into the base manim implementation at this time! But therefore it can render enormous meshes fast.\nThe `TriangleManim2DMesh` from `triangle_mesh` implements further functions that are only reasonable for triangle meshes. (e.g. Delaunay)\n\nAll these Mesh-Renders are based on out own `Mesh`-Class, in `data_models`, which should implement a multitude of functions\n\n[//]: #  (TODO create basic use-case with code)\n\n\n## Example\n\n[//]: # (TODO create working example + video)\n\nIn venv Run one of the minimal test examples: `manim tests/test_scene.py ConeScene`.\nMultiple other examples can be found in the `tests/test_scene.py` file.\n\n\n## Development\nIn PyCharm set `./src/`-folder as project sources root and `./tests/`-folder as tests sources root if necessary.\n\nActivate the poetry venv: `cd ./manim_meshes/`, then `poetry shell`\n\nInstall: `poetry install`\nIf you get errors, it is possible that you have to pip install `pycairo` and or `manimpango` manually, depending on your setup. Make sure to run `poetry install` until there are no more errors!\n\nUpdate packages and your own .lock file: `poetry update`\n\nIf you implemented some features, update version using the matching poetry command: `poetry version prerelease|patch|minor|major`\nSee the Poetry [Documentation](https://python-poetry.org/docs/cli/#version).\n\nEven though if the CI works properly, Publish on master branch is automatically, it can be done manually with: `poetry publish --build`\n\n### Debugging\nLike with basic manim, create an executable Python file with something around:\n\n```python\nfrom tests.test_scene import SnapToGridScene\nif __name__ == "__main__":\n    scene = SnapToGridScene()\n    scene.render()\n```\n\nThen debug the file and place breakpoints as expected. May not work with the "renderer=opengl" flag that is necessary for some scripts.',
    'author': 'Brizar',
    'author_email': 'martin.steinborn@stud.tu-darmstadt.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bmmtstb/manim-meshes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
