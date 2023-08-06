# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pouty', 'pouty.stdlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pouty',
    'version': '1.0.0',
    'description': 'C++-style IO in Python!',
    'long_description': '# Pouty: a very silly library bringing weird C++ features to Python since 2022\n\nDo you like Python? Wanna use std::cout in it? No? I didn\'t ask!\n\n`pouty` is a Python package that will make you pout with it\'s ability to use C++ style IO in Python.\n\n## FAQ:\n\n- **Is it fast?**\n  No.\n- **Does C++ I/O even make sense in this context?**\n  That\'s for you to judge.\n- **Is it faster than Python\'s print()?**\n  While it may *occasionally* avoid a string creation or contcatenation, it does so through multiple operator overloads and several function calls + type checks. Therefore, no.\n- **Why is C++\'s iostream fast?**\n  C++ is a compiled language with static typing and function call inlining.\n- **Why make this?** \n  Because I can.\n\n\n## Example code (`examples/test.py`):\n\n```python\nfrom pouty.iostream import *;\nimport random;\n\nstd.cout << "Hello, world!" << std.endl\n\nclass CustomOutput: #custom operator<< and operator>> overload supported\n    is_pouty_stream = True\n    def __init__(self) -> None:\n        self.x = ref(0)\n        pass\n\n    def __lshift__(self, other: any) -> None:\n        other << self.x[...]\n    \n    def __rshift__(self, other: any) -> None:\n        other >> self.x\n\n# Python [unfortunately, perhaps fortunately!] does not have implicit reference parameters.\nx = ref(0)\nstd.cin >> x\nstd.cout << x << std.endl # uses the __str__ method of ref\nstd.cout << x[...] << std.endl # dereferences the ref and prints the int\n\nx = CustomOutput()\nstd.cin >> x\nstd.cout << x << std.endl\n\nx = random.random() #precision is supported too!\nstd.cout << x << std.endl\nstd.cout << std.precision(3) \nstd.cout << x << std.endl\n\n\nusing_namespace(globals(), "std")\ncout << "Hello, world!" << endl # bringing namespace pollution into Python since 2022 :)\n\nfrom pouty.stdlib.h import *;\n\nprintf("%s", "Hello, world!")\nprintf("%d", 123) #note that precision is not supported yet here (feel free to contrubute it)\nputs("Hello, world!")\n```\n\n## Installation\n\n`pip install pouty`\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss the change.\n',
    'author': 'Om Duggineni',
    'author_email': 'omduggineni@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
