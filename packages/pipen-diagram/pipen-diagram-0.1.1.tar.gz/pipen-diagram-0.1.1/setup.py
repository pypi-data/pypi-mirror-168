# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_diagram']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20,<0.21', 'pipen>=0.3,<0.4']

entry_points = \
{'pipen': ['diagram = pipen_diagram:PipenDiagram']}

setup_kwargs = {
    'name': 'pipen-diagram',
    'version': '0.1.1',
    'description': 'Draw pipeline diagrams for pipen.',
    'long_description': '# pipen-diagram\n\nDraw pipeline diagrams for [pipen][1].\n\n## Features\n\n- Different coloring for different roles of processes (start, end, etc)\n- Diagram theming\n- Hiding processes from diagram\n\n## Configurations\n\n- `diagram_theme`: The name of the theme to use, or a dict of a custom theme.\n  - See `pipen_diagram/diagram.py` for the a theme definition\n- `diagram_savedot`: Whhether to save the dot file (for debugging purpose)\n- `diagram_hide`: Process-level item, whether to hide current process from the diagram\n\n## Installation\n\n```\npip install -U pipen-diagram\n```\n\n## Enabling/Disabling the plugin\n\nThe plugin is registered via entrypoints. It\'s by default enabled. To disable it:\n`plugins=[..., "no:diagram"]`, or uninstall this plugin.\n\n## Usage\n\n`example.py`\n```python\nfrom pipen import Proc, Pipen\n\nclass Process(Proc):\n    input = \'a\'\n    output = \'b:{{in.a}}\'\n\nclass P1(Process):\n    input_data = [1]\n\nclass P2(Process):\n    requires = P1\n\nclass P3(Process):\n    requires = P2\n    plugin_opts = {"diagram_hide": True}\n\nclass P4(Process):\n    requires = P3\n\nPipen().run(P1)\n```\n\nRunning `python example.py` will generate `pipen-0_results/diagram.svg`:\n\n![diagram](./diagram.png)\n\n[1]: https://github.com/pwwang/pipen\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwwang/pipen-diagram',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
