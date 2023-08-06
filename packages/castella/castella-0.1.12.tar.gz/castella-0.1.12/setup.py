# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['castella']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "glfw"': ['glfw>=2.5.3,<3.0.0'],
 ':extra == "glfw" or extra == "sdl"': ['skia-python>=87.4,<88.0',
                                        'darkdetect>=0.5.1,<0.6.0'],
 ':extra == "sdl"': ['glcontext>=2.3.6,<3.0.0', 'pysdl2-dll>=2.0.20,<3.0.0'],
 'glfw': ['PyOpenGL>=3.1.5,<4.0.0'],
 'sdl': ['PySDL2>=0.9.11,<0.10.0', 'zengl>=1.2.2,<2.0.0']}

setup_kwargs = {
    'name': 'castella',
    'version': '0.1.12',
    'description': 'Castella is a pure Python cross-platform UI framework',
    'long_description': '# Castella\nCastella is a pure Python cross-platform UI framework.\n\n<img src="https://user-images.githubusercontent.com/6240399/174487936-8484be0e-b2b5-433c-9416-594c0fd57f3a.png" style="height: 1em;"></img> [Documentation Site](https://i2y.github.io/castella) <img src="https://user-images.githubusercontent.com/6240399/174487787-7099167f-a8ad-42e8-9362-c19c84dc81be.png" style="height: 1em;"></img> [Examples](examples)\n\n## Goals\n\nThe primary final goal of Castella is to provide features for Python programmers easy to create a GUI application for several OS platforms and web browsers in a single most same code as possible as. The second goal is to provide a UI framework that Python programmers can easily understand, modify, and extend as needed.\n(Stated on May 25, 2022: This goal is the final goal. Currently this framework is in the super early stage, so this goal is far away. I hope to get much closer to the goal in a few months or a year by improving the implementation or documentation a little bit every day as much as possible.)\n\n## Features\n- The core part as a UI framework of Castella is written in only Python. It\'s not a wrapper for existing something written in other programing languages.\n- Castella allows human to define UI declaratively in Python.\n- Castella provides hot-reloading or hot-restarting on development.\n- Dark mode is supported. If the runtime environment is in dark mode, Castella app\'s UI appearance will automatically be styled in dark mode.\n- Castella utilizes GPU via dependent libraries.\n\n## Dependencies\n- For desktop platforms, Castella is standing on existing excellent python bindings for window management library (GLFW or SDL2) and 2D graphics library (Skia).\n- For web browsers, Castella is standing on awesome Pyodide/PyScript and CanvasKit (Wasm version of Skia).\n\n## Installation\nhttps://i2y.github.io/castella/getting-started/\n\n## An example of code using Castella\n\n```python\nfrom castella import App, Button, Column, Component, Row, State, Text\nfrom castella.frame import Frame\n\n\nclass Counter(Component):\n    def __init__(self):\n        super().__init__()\n        self._count = State(0)\n\n    def view(self):\n        return Column(\n            Text(self._count),\n            Row(\n                Button("Up", font_size=50).on_click(self.up),\n                Button("Down", font_size=50).on_click(self.down),\n            ),\n        )\n\n    def up(self, _):\n        self._count += 1\n\n    def down(self, _):\n        self._count -= 1\n\n\nApp(Frame("Counter", 800, 600), Counter()).run()\n```\n\nhttps://user-images.githubusercontent.com/6240399/171010621-8c0068d2-eb90-4332-8a1b-115291053d42.mp4\n\nYou can see some other examples in [examples](examples) directory.\n\n## Supported Platforms\nCurrently, Castella theoretically should support not-too-old versions of the following platforms.\n\n- Windows 10/11\n- Mac OS X\n- Linux\n- Web browsers\n\n## License\nMIT License\n\nCopyright (c) 2022 Yasushi Itoh\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'Yasushi Itoh',
    'author_email': 'i2y@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/i2y/castella',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
