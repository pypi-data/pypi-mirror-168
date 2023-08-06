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
    'version': '0.0.1',
    'description': 'Filelister is a Python package that makes working with filelists (yes, lists of files) easy.',
    'long_description': '# Filelister\n\n### Filelister is a Python package that makes working with filelists (yes, lists of files) easy.\n\n```python\nimport filelister as fs\n```\n\n# Basic Usage\n\n## Creating a Filelist\n\n### From Data\nYou can create a Filelist object from a `list`, `set`, `tuple`, `Filelist` object, or `path` to directory.\n\n```python\nmy_filelist = fs.Filelist([\'../file_01.jpg\', \'../file_02.jpg\'])\n\nmy_other_filelist = fs.Filelist(\'path/to/directory/\')\n```\n\n### From System Files\nYou can also create a Filelist object by reading from a filelist saved on your system.\n\n```python\nmy_filelist = fs.read_filelist(\'path/to/filelist.txt\')\n```\n\n## Working with Filelists\n\n### Manipulating a Filelist\nFilelists support a number of conversions, including conversions to a native python list, to a relative filelist, and to an absolute filelist.\n\n```python\nmy_filelist.to_list()\n\nmy_filelist.to_abs()\n\nmy_filelist.to_rel()\n```\nThese commands can also be chained:\n```python\nmy_filelist.to_abs().to_list()\n```\n\n### In and Contains\nFilelists support a cointains method, as well as the python `in` operator.\n```python\nmy_filelist.contains(\'path/to/file\')\n\n\'path/to/file\' in my_filelist\n```\n\n### Indexing and Slicing\nA filelist can also be indexed and sliced like a normal python list. This will always return a native python list.\n```python\nmy_filelist[1] == \'path/to/file.txt\'\n\nmy_filelist[:3] == [\'path/to/file01.txt\', \'path/to/file02.txt\', \'path/to/file03.txt\']\n```\n\n## Saving a Filelist\n\n### Arguments\n`outfile`: specify a path to the location in which to write the filelist.\n`output_type`: specify the type of filelist to write. Options include `\'abs\'`, `\'rel\'`, and `\'na\'` (see below).\n`compressed`: accepts a boolean. Pass `compressed=True` to write a compressed filelist.\n\n### Usage\n```python\nmy_filelist.save(\'filelists/my_filelist.txt\', output_type=\'abs\', compressed=True)\n```\nNote that when saving a relative filelist, the filepaths are converted to be relative to the location of the filelist.\n\n\n### Compression\nA filelist can be stored using custom zlib compression by using\n```python\nmy_filelist.save(outfile=\'compressed_filelist.zz\', compressed=True)\n```\nThis filelist can then be read using\n```python\nfs.read_filelist(\'compressed_filelist.zz\', compressed=True)\n```\nDue to the nature of the compression, a compressed filelist should only be read by filelister.\n\n### Types of Filelists\nFilelister supports three formats of filelists: Absolute, Relative, and "na"\n#### Absolute\n `abs` refers to an absolute filelist\n```python\n[\'path/to/file_01.txt\', \'path/to/file_02.txt\', \'path/to/file_03.txt\']\n```\n#### Relative\n`rel` refers to a relative filelists\n\n```python\n[\'../file_01.txt\', \'../file_02.txt\', \'../file_03.txt\']\n```\n#### na\n`na` refers to a filelist that is stored with no context, where filepaths are ignored and only filenames are stored\n```python\n[\'file_01.txt\', \'file_02.txt\', \'file_03.txt\']\n```\n\n\n# Installation\n\n## pip (PyPi)\n```bash\npip install filelister\n```\n\n## Anaconda\n*Coming soon*\n',
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
