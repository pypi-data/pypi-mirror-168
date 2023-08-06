# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filelister']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'filelister',
    'version': '0.0.0',
    'description': 'Filelister is a Python package that makes working with filelists (yes, lists of files) easy.',
    'long_description': '# Filelister\n\n### Filelister is a Python package that makes working with filelists (yes, lists of files) easy.\n\n```python\nimport filelister as fs\n```\n\n### Contents\n- [Basic Usage](#basic-usage)\n- [Installation](#installation)\n- [Contributors](#contributors)\n- [API](#API)\n\n# Basic Usage\n\n## Types of Filelists\nFilelister supports three formats of filelists: Absolute, Relative, and "na"\n### Absolute\n `abs` refers to an absolute filelist\n```python\n[\'path/to/file_01.txt\', \'path/to/file_02.txt\', \'path/to/file_03.txt\']\n```\n### Relative\n`rel` refers to a relative filelists\n\n```python\n[\'../file_01.txt\', \'../file_02.txt\', \'../file_03.txt\']\n```\n### na\n`na` refers to a filelist that is stored with no context, where filepaths are ignored and only filenames are stored\n```python\n[\'file_01.txt\', \'file_02.txt\', \'file_03.txt\']\n```\n\n## Creating a Filelist\n\n### From Data\nYou can create a Filelist object from a list, set, tuple, Filelist object, or path to directory.\n\n```python\nmy_filelist = fs.Filelist([\'../file_01.jpg\', \'../file_02.jpg\'])\n\nmy_other_filelist = fs.Filelist(\'path/to/directory\')\n```\n\n### From System Files\nYou can also create a Filelist object by reading from a filelist saved on your system.\n\n```python\nmy_filelist = fs.read_filelist(\'path/to/filelist.txt\')\n```\n\n\n## Saving a Filelist\n### Arguments\n`outfile`: specify a path to the location in which to write the filelist.  \n`output_type`: specify the type of filelist to write. Options include `\'abs\'`, `\'rel\'`, and `\'na\'`.  \n`compressed`: accepts a boolean. Pass `compressed=True` to write a compressed filelist.  \n### Usage\n```python\nmy_filelist.save(\'filelists/my_filelist.txt\', output_type=\'abs\', compressed=True)\n```\nNote that when saving a relative filelist, the filepaths are converted to be relative to the location of the filelist.\n\n\n## Compression\nA filelist can be stored using custom zlib compression by using\n```python\nmy_filelist.save(outfile=\'compressed_filelist.zz\', compressed=True)\n```\nThis filelist can then be read using\n```python\nfs.read_filelist(\'compressed_filelist.zz\', compressed=True)\n```\nDue to the nature of the compression, a compressed filelist should only be read by filelister.\n\n## Working with Filelists\n\n### Manipulating a Filelist\nFilelists support a number of conversions, including conversions to a native python list, to a relative filelist, and to an absolute filelist.\n```python\nmy_filelist.to_list()\n\nmy_filelist.to_abs()\n\nmy_filelist.to_rel()\n```\nThese commands can also be chained:\n```python\nmy_filelist.to_abs().to_list()\n```\nFilelists support a cointains method, as well as the python `in` operator.\n```python\nmy_filelist.contains(\'path/to/file\')\n\n\'path/to/file\' in my_filelist\n```\n\nA filelist can also be indexed and sliced like a normal python list. This will always return a native python list.\n```python\nmy_filelist[1] == \'path/to/file.txt\'\n\nmy_filelist[:3] == [\'path/to/file01.txt\', \'path/to/file02.txt\', \'path/to/file03.txt\']\n```\n\n# The Vision\nThis tool was created to make sharing and handling filelists simple and easy for everyone.\n## Runtime/Storage efficiency info here?\n- O(1) get/lookup\n- O(n) instantiaton\n- Efficient data storage`\n# Installation\n\n## pip (local)\nYou can install this package locally via Github and pip.\n\n```bash\ngit clone https://github.com/burkecp/filelister.git\ncd filelister\npip install -e .\n```\n## pip (PyPi)\n*Coming soon*\n\n## Anaconda\n*Coming soon*\n\n# Contributors\n\n## Authors\nSimon Burke\nChristian Burke\nRefik Anadol Studio\n\n## Spec\n### Use Cases\n1. Simple read and write\n2. Ability to check if a filelist contains a path\n3. Ability to create batches from a filelist (TODO)\n4. Ability to resolve correct output paths for a relative filelist\n5. Ability to verify contents of a filelist (TODO)\n6. Convert relative/absolute filelists\n7. Ability to compare filelists (TODO)\n8. Ability to perform list + set methods on a filelist (TODO)\n\n### Runtimes\n1. O(n) read and O(n) write\n2. O(1) contains\n3. O(n) iteration\n\n# API\n\n## In Progress\n\n### Arithmetic Operations\n\n### Set Operations\n',
    'author': 'NaN Developers',
    'author_email': 'nanwtf@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
