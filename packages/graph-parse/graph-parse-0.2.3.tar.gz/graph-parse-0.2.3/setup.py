# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graph_parse']

package_data = \
{'': ['*']}

install_requires = \
['mypy', 'pydantic', 'pydash', 'pytest']

setup_kwargs = {
    'name': 'graph-parse',
    'version': '0.2.3',
    'description': '',
    'long_description': '# Graph Parse\n\nGraph Parse is a package for decoupling and abstracting the various stages of parsing such as mapping, transforming and casting.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install graph-parse.\n\n```bash\npip install graph-parse\n```\n\n## Usage\n\n```python\n\nfrom datetime import datetime\nfrom graph_parse.models import Node, Edge, Graph\nfrom graph_parse.helpers import instantiate_many\n\n\nclass PersonOld(Node):\n    name: str \n    dob: datetime\n\nclass PersonNew(Node):\n    name: str \n    age: int\n\n\ndef dob_to_age(dob: datetime) -> int:\n    today = datetime.today()\n    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))\n\nold_person = PersonOld()\nnew_person = PersonNew() \n\ngraph = Graph(\n    edges=[\n        Edge(old_person.name(), new_person.name()),\n        Edge(old_person.dob(), new_person.age(), function=dob_to_age)\n    ]\n)\n\nold_person_data = PersonOld(name="James", dob=datetime(1997, 6, 10))\nresponse = graph.traverse(old_person_data)\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://opensource.org/licenses/MIT)',
    'author': 'james',
    'author_email': 'jamesnarayanrao@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
