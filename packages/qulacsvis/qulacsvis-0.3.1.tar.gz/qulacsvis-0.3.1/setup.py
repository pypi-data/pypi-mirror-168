# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qulacsvis', 'qulacsvis.utils', 'qulacsvis.visualization']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'Qulacs>=0.5.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.22.0,<2.0.0',
 'scipy>=1.9.1,<2.0.0',
 'temp>=2020.7.2,<2021.0.0']

setup_kwargs = {
    'name': 'qulacsvis',
    'version': '0.3.1',
    'description': 'visualizers for qulacs',
    'long_description': '# qulacs-visualizer\n\n[![CI](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml) [![Build and Deploy Documentation](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml) [![PyPI version](https://badge.fury.io/py/qulacsvis.svg)](https://badge.fury.io/py/qulacsvis) [![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n\nqulacs-visualizer is a quantum circuit drawing library for [qulacs](https://github.com/qulacs/qulacs). This library only supports Python. Not available in C/C++.\n\nqulacs-visualizer supports the following methods.\n\n- Text-Based Drawing\n- Matplotlib Drawing\n  - using [matplotlib](https://github.com/matplotlib/matplotlib)\n- LaTeX Drawing\n  - using LaTeX and the [qcircuit package](https://github.com/CQuIC/qcircuit)\n\n\n## Quick Install\n\nInstall using `pip` from PyPI:\n\n```\npip install qulacsvis\n```\n\n## Example\n\n\nFor more information, see the [documentation](https://qulacs-osaka.github.io/qulacs-visualizer/index.html).\nThe documentation describes the [other options available](https://qulacs-osaka.github.io/qulacs-visualizer/options.html).\n\n### Text-Based Drawing\n\nIn text-based mode, draws the circuit as ASCII art. This mode is the default behavior.\n\n```py\nfrom qulacs import QuantumCircuit\nfrom qulacsvis import circuit_drawer\n\n# Build a quantum circuit\ncircuit = QuantumCircuit(3)\ncircuit.add_X_gate(0)\ncircuit.add_Y_gate(1)\ncircuit.add_Z_gate(2)\ncircuit.add_dense_matrix_gate(\n    [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]\n)\ncircuit.add_CNOT_gate(2, 0)\ncircuit.add_X_gate(2)\n\n# Draw a quantum circuit\ncircuit_drawer(circuit)\n```\n```\n   ___     ___     ___\n  | X |   |DeM|   |CX |\n--|   |---|   |---|   |----------\n  |___|   |   |   |___|\n   ___    |   |     |\n  | Y |   |   |     |\n--|   |---|   |-----|------------\n  |___|   |___|     |\n   ___              |      ___\n  | Z |             |     | X |\n--|   |-------------●-----|   |--\n  |___|                   |___|\n```\n\n### Matplotlib Drawing\n\nTo use another drawing method, you can specify it by setting a value to the `output_method` argument of the `circuit_drawer()` function. For matplotlib drawing, set `output_method="mpl"`.\n\n```py\ncircuit_drawer(circuit, "mpl")\n```\n\n![circuit_matplotlib_drawing.png](doc/source/_static/circuit_matplotlib_drawing.png)\n\n## LaTeX Drawing\n\nFor LaTeX drawing, set `output_method="latex"`.\n\n```py\ncircuit_drawer(circuit, "latex")\n```\n\n![circuit_latex_drawing.png](doc/source/_static/circuit_latex_drawing.png)\n\nIf you want to output LaTeX code, set `output_method="latex_source"`.\n\n```py\nprint(circuit_drawer(circuit, "latex_source"))\n```\n\n```latex\n\\documentclass[border={-2pt 5pt 5pt -7pt}]{standalone}\n\\usepackage[braket, qm]{qcircuit}\n\\usepackage{graphicx}\n\n\\begin{document}\n    \\Qcircuit @C=1.0em @R=0.7em @!R{ \\\\\n        \\nghost{ q_{0} : } & \\lstick{ q_{0} : } & \\gate{X} & \\multigate{1}{DeM} & \\targ & \\qw & \\qw\\\\\n        \\nghost{ q_{1} : } & \\lstick{ q_{1} : } & \\gate{Y} & \\ghost{DeM} & \\qw & \\qw & \\qw\\\\\n        \\nghost{ q_{2} : } & \\lstick{ q_{2} : } & \\gate{Z} & \\qw & \\ctrl{-2} & \\gate{X} & \\qw\\\\\n    }\n\\end{document}\n```\n\n### Requirement\n\nIf you want to use LaTeX Drawing, you need to have a local environment where you can run LaTeX (pdflatex).\nYou will also need the [qcircuit package](https://github.com/CQuIC/qcircuit).\n[TeX Live](https://www.tug.org/texlive/) and [MiKTeX](https://miktex.org/) have the qcircuit package installed by default.\n\n## License\n\n[MIT License](LICENSE)\n\n## Contributors\n\nWe use [qqcd](https://github.com/mf-22/qqcd) for text-based drawing, a drawing library developed by [@mf-22](https://github.com/mf-22). Thank you.\n',
    'author': 'Qulacs-Osaka',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Qulacs-Osaka/qulacs-visualizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
