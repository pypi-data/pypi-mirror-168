# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pyresourcehandler']
setup_kwargs = {
    'name': 'pyresourcehandler',
    'version': '1.0.4',
    'description': '',
    'long_description': '# pyResourceHandler: Small package to help with resource handling \n\npyResourceHandler provides a few functions to easily handle resources.\n\nIt requires Python 3.9+ to run.\n\n## Key Features\n* Small package\n* 100% coverage\n* Easy to use \n* Functions are type-hinted.\n* Handles regular files, directories and even malformed python files as resources/assets.\n\n## How to Install\nInstall from PyPi \n> pip install pyResourceHandler\n   \nImport \'extractFile\' and/or \'extractDir\' \n> from pyResourceHandler import extractFile\n> \n## How to Use\n\n1.The module should have a root directory with one of the following names:\n\n* data\n* resources\n* assets\n\n2.Place files and/or directories within your resource directory.\n\n3.Done!\n\n* To extract a file\n\n> extractFile(\n    "Example_Module",\n    "file_example.txt",\n    r"C:\\Users\\user\\Desktop\\your_file.txt"\n)\n\n* To extract a directory\n\n> extractDirectory(\n    "Example_Module",\n    "directory_example",\n    r"C:\\Users\\user\\Desktop\\your_directory"\n)\n\n1st Argument - Module import as a string.\\\n2nd Argument - Path to file/directory\\\n3rd Argument - Output path for file/directory\n\nDo note, the above functions will not overwrite an existing file by default.\\\nTo enable overwriting, set the argument named **overwrite** argument to True when invoking the functions.\n\n## Why?\n\nWriting similar pieces of code to access non-Python files across projects can be tedious.\n\nThis reduces boilerplate code for repetitive operations down to a single function call.\n\n',
    'author': 'icySnippets',
    'author_email': 'admin@icysnippets.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
