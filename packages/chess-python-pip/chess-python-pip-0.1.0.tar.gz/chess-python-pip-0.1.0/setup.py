# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chess_python']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0']

setup_kwargs = {
    'name': 'chess-python-pip',
    'version': '0.1.0',
    'description': 'Python implementation of the game of chess.',
    'long_description': '# Introduction\n\n## Performance\n\nUsing `python3 -m cProfile -o prof.txt tree.py -h` for profiling and `snakeviz prof.txt` to\nvisualize.\n\nPerft(3) initial positions `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1` (8902\npositions, reference time 0.05 with `python-chess`:\n\n- 1.25 s (first)\n- 0.79 s (moving `get_positions_attacking_pieces` to optimizer initialization and update, not when\n  checking if move is legal)\n- 0.70 removing np.array from list of moves (does not make a lot of sense)\n- 0.55 removing more np.arrays\n\n# TODO:\n\n    - [X] Include tests for perft in different positions\n    - [ ] Utils if there is a mismatch in positions\n    - [ ] Improve performance\n    - [ ] Improve overall code quality (clarity, choose right data structure for the job)\n    - [X] Automate release with github action to pip\n    - [ ] Explore pypy\n',
    'author': 'pacanada',
    'author_email': 'pereirapcanada@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
