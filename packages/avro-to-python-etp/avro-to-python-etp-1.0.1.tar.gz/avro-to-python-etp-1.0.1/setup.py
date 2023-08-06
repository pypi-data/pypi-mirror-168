# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avro_to_python_etp',
 'avro_to_python_etp.classes',
 'avro_to_python_etp.reader',
 'avro_to_python_etp.utils',
 'avro_to_python_etp.utils.avro',
 'avro_to_python_etp.utils.avro.files',
 'avro_to_python_etp.utils.avro.types',
 'avro_to_python_etp.writer']

package_data = \
{'': ['*'],
 'avro_to_python_etp': ['templates/*',
                        'templates/fields/*',
                        'templates/files/*',
                        'templates/imports/*',
                        'templates/partials/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'anytree>=2.8.0,<3.0.0',
 'avro>=1.11.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'nested-lookup>=0.2.25,<0.3.0',
 'typingx>=0.6.0,<0.7.0',
 'wheel>=0.37.1,<0.38.0']

entry_points = \
{'console_scripts': ['avpr-to-avsc = avro_to_python_etp.avpr_to_avsc:main',
                     'avro-to-python-etp = avro_to_python_etp.cli:main']}

setup_kwargs = {
    'name': 'avro-to-python-etp',
    'version': '1.0.1',
    'description': 'Light tool for compiling avro schema files (.avsc) to python classes making using avro schemata easy.',
    'long_description': '==================\navro-to-python-etp\n==================\n\navro-to-python-etp is a light tool for compiling avro schema files (.avsc) to python classes making using avro schemata easy.\n\n\n* Free software: MIT license\n* Documentation: https://avro-to-python-etp.readthedocs.io.\n\nInstallation\n^^^^^^^^^^^^\n\nPip install (recommended)\n-------------------------\nTo install avro-to-python-etp, run this command in your terminal:\n\n.. code-block:: console\n\n    $ pip install avro-to-python-etp\n\nInstall From Source ()\n----------------------\n\nThe sources for avro-to-python-etp can be downloaded source as well.\n\nClone the public repository:\n\n.. code-block:: console\n\n    $ git clone git://github.com/srserves85/avro-to-python-etp\n\n\nOnce you have a copy of the source, you can install it with:\n\n\n.. code-block:: console\n\n    $ python setup.py install\n\nor\n\n.. code-block:: console\n\n    $ pip install -e .\n\n\nExamples\n^^^^^^^^\n\nMajority of the use of avro-to-python-etp is assumed to be used as a cli, but you can still import and use the python classes under the hood as well.\n\nCLI (without --pip)\n-------------------\nTo use the cli, here is the available cli commands:\n\n.. code-block:: bash\n\n    avro-to-python-etp [source] [target]\n        Options:\n            --pip TEXT              make package pip installable using this name\n            --author TEXT           author name of the pip installable package\n            --package_version TEXT  version of the pip intallable package  [default: 0.1.0]\n            --help                  Show this message and exit\n\n\nThe above will compile the avsc files and convert the to python classes found in [path_to_target_directory]\n\nAn example of doing this is the following:\n\n.. code-block:: bash\n\n    avro-to-python-etp [path_to_source_avsc_files] [path_to_target_directory]\n\n\nIf you run the above on a valid avro avsc file, you should then be able to import them as you would in the avro idl namespace Here is an example of a single avsc record from the namespace: *name.space* and name: *RecordClass*:\n\n.. code-block:: python\n\n    from name.space import RecordClass\n\n    record = RecordClass({\'foo\': True, \'bar\': \'true\', \'baz\': 10, \'food\': \'CHOCOLATE\'})\n\n\nCLI (with --pip)\n----------------\nYou can also choose to make compiled avro packages ***pip installable*** by adding the "--pip" flags. An example of this is the following:\n.. code-block:: bash\n\n    avro-to-python-etp [path_to_source_avsc_files] [path_to_target_directory] --pip test_avro\n\nBy running this, you should be able to pip install the above package you created from the target directory you specified by running:\n\n.. code-block:: bash\n\n    pip install -e path_to_target_directory\n\nNow that you have the package installed, you can import it by it\'s package name and namespace. Here is the same example of the same avsc from above, only with a pip package of *test_avro*:\n\n.. code-block:: python\n\n    from test_avro.name.space import RecordClass\n\n    record = RecordClass({\'foo\': True, \'bar\': \'true\', \'baz\': 10, \'food\': \'CHOCOLATE\'})\n\n\navro-to-python-etp in a Script\n------------------------------\nYou can also use the reader and writer packages in avro-to-python-etp as you would any other python package. Avro to python is split between a *reader* and *writer* classes. avro-to-python-etp treates namespaces as acyclic trees and uses depth first search to ensure no duplication or namespace collisions on read and write. An example useage is below:\n\n.. code-block:: python\n\n    from avro_to_python.reader import AvscReader\n    from avro_to_python.writer import AvroWriter\n\n    # initialize the reader object\n    reader = AvscReader(directory=\'tests/avsc/records/\')\n\n    # generate the acyclic tree object\n    reader.read()\n\n    # initialize the writer object\n    writer = AvroWriter(reader.file_tree, pip=\'test_pip\')\n\n    # compile python files using \'tests/test_records as the namespace root\'\n    writer.write(root_dir=\'tests/test_records\')\n\n\n\nRoadmap\n^^^^^^^\n\nReader\n\n- [X] Create Namespace Trees on nested namespaces\n- [X] Read Record and Enum File\n- [X] Primitive types\n- [X] Array Types\n- [X] Union types\n- [X] References to other files\n- [X] Map Types\n- [ ] Logical Types (Currently just converts to primitive types)\n\nWriter\n\n- [X] Base Schema Writer\n- [X] Base Record Schema\n- [X] Base Enum Schema\n- [X] Primitive Types Schema\n- [X] Array Types Schema\n- [X] Union Types Schema\n- [X] Map Types\n- [ ] Logical Types Schema (Currently just converts to primitive types)\n- [X] Add configs to pip install package\n\nCLI\n\n- [X] Wrap Writer and Reader into one cli commmit\n- [X] Add pip install option (would include all files to pip install compiled package)\n- [ ] Add better --help documentation\n\nDocumentation\n\n- [ ] Document reader class\n- [ ] Document writer class\n- [ ] Document cli',
    'author': 'Scott Rothbarth',
    'author_email': 'srserves85@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/geosiris-technologies/avro-to-python-etp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
