# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synbio_schema']

package_data = \
{'': ['*']}

install_requires = \
['cruft>=2.11.1,<3.0.0',
 'db-to-sqlite>=1.4,<2.0',
 'linkml-runtime>=1.1.24,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'synbio-schema',
    'version': '0.0.1',
    'description': 'A schema for synthetic biology, inspired by IARPA FELIX',
    'long_description': '# synbio-schema\n\nA schema for synthetic biology, inspired by IARPA FELIX\n\n## Website\n\n* [https://semantic-synbio.github.io/synbio-schema](https://semantic-synbio.github.io/synbio-schema)\n\n## Repository Structure\n\n* [examples/](examples/) - example data\n* [project/](project/) - project files (do not edit these)\n* [src/](src/) - source files (edit these)\n    * [synbio_schema](src/synbio_schema)\n        * [schema](src/synbio_schema/schema) -- LinkML schema (edit this)\n* [datamodel](src/synbio_schema/datamodel) -- Generated python datamodel\n* [tests](tests/) - python tests\n\n## Developer Documentation\n\n<details>\nUse the `make` command to generate project artefacts:\n\n- `make all`: make everything\n- `make deploy`: deploys site\n\n</details>\n\n## Credits\n\nthis project was made with [linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)\n',
    'author': 'Mark Andrew Miller',
    'author_email': 'MAM@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
