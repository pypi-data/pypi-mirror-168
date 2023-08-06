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
    'version': '0.1.1',
    'description': 'Python implementation of the game of chess.',
    'long_description': '# Introduction\n\nPython implementation of chess game in less than 1000 lines of code.\n\nThere is also a work in progress for the cli based game (`python -m chess_python.game`).\n\nDisclaimer: it is missing api for checkmate and stalemates\n\n# Usage\n\n```\npip install chess-python-pip\n```\n\n```python\n#examples/example_01.py\nfrom chess_python.chess import Chess\nchess = Chess(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0") # Default\nprint(chess)\nprint(chess.legal_moves())\nchess.move("e2e4")\nprint(chess)\n```\n\noutputs:\n\n```\nPlayer to move: White\nMove count: 0\n8 || r | n | b | q | k | b | n | r |\n-----------------------------------\n7 || p | p | p | p | p | p | p | p |\n-----------------------------------\n6 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n5 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n4 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n3 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n2 || P | P | P | P | P | P | P | P |\n-----------------------------------\n1 || R | N | B | Q | K | B | N | R |\n-----------------------------------\n-----------------------------------\n  || a | b | c | d | e | f | g | h\n\n[\'b1a3\', \'b1c3\', \'g1f3\', \'g1h3\', \'a2a3\', \'a2a4\', \'b2b3\', \'b2b4\', \'c2c3\', \'c2c4\', \'d2d3\', \'d2d4\', \'e2e3\', \'e2e4\', \'f2f3\', \'f2f4\', \'g2g3\', \'g2g4\', \'h2h3\', \'h2h4\']\nPlayer to move: Black\nMove count: 1\n8 || r | n | b | q | k | b | n | r |\n-----------------------------------\n7 || p | p | p | p | p | p | p | p |\n-----------------------------------\n6 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n5 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n4 ||   |   |   |   | P |   |   |   |\n-----------------------------------\n3 ||   |   |   |   |   |   |   |   |\n-----------------------------------\n2 || P | P | P | P |   | P | P | P |\n-----------------------------------\n1 || R | N | B | Q | K | B | N | R |\n-----------------------------------\n-----------------------------------\n  || a | b | c | d | e | f | g | h\n```\n\n# DEV section:\n\n## Performance tracking\n\nUsing `python3 -m cProfile -o prof.txt tree.py -h` for profiling and `snakeviz prof.txt` to\nvisualize.\n\nPerft(3) initial position `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1` (8902\npositions, reference time 0.05 s with\n[`python-chess`](https://python-chess.readthedocs.io/en/latest/):\n\n- 1.25 s (first)\n- 0.79 s (moving `get_positions_attacking_pieces` to optimizer initialization and update, not when\n  checking if move is legal)\n- 0.70 s removing np.array from list of moves (does not make a lot of sense)\n- 0.55 s removing more np.arrays\n\n## TODO:\n\n- [x] Include tests for perft in different positions\n- [ ] Include utils if there is a mismatch in positions tree with reference implementation\n- [ ] Improve performance\n- [ ] Improve overall code quality (clarity, choose right data structure for the job)\n- [x] Automate release with github action to pip\n- [ ] Explore pypy\n',
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
