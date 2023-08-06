# Graph Parse

Graph Parse is a package for decoupling and abstracting the various stages of parsing such as mapping, transforming and casting.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install graph-parse.

```bash
pip install graph-parse
```

## Usage

```python

from datetime import datetime
from graph_parse.models import Node, Edge, Graph
from graph_parse.helpers import instantiate_many


class PersonOld(Node):
    name: str 
    dob: datetime

class PersonNew(Node):
    name: str 
    age: int


def dob_to_age(dob: datetime) -> int:
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

old_person = PersonOld()
new_person = PersonNew() 

graph = Graph(
    edges=[
        Edge(old_person.name(), new_person.name()),
        Edge(old_person.dob(), new_person.age(), function=dob_to_age)
    ]
)

old_person_data = PersonOld(name="James", dob=datetime(1997, 6, 10))
response = graph.traverse(old_person_data)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://opensource.org/licenses/MIT)