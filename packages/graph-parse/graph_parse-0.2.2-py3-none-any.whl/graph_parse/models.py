from __future__ import annotations
from typing import Callable, List, Set, Tuple, Union, Optional
from pydash.objects import get, set_
from pydantic import BaseModel
from time import time_ns

from graph_parse.enums import ComparitiveOperationEnum, TraversalEventEnum
from graph_parse.helpers import iterables_intersect, nested_getattr, camel_to_snake, flatten, format_alias


class Node:
    __path: List[str]
    
    def __init__(self, path=[], value=None, **kwargs):
        self.__path = path or [self.class_snake_name]
        self.__value = value or self

        globals()[f"node_{self.class_snake_name}"] = self.__class__

        for name in self.__annotations__:
            if name.startswith("_Node__"):
                continue

            new_path = self.__path + [name]
            new_value = kwargs.get(format_alias(name))
            new_kwargs = new_value.to_dict() if isinstance(new_value, Node) else {}

            private_name = f"_{name}"

            setattr(self, private_name, Node(path=new_path, value=new_value, **new_kwargs))
            setattr(self.__class__, name, property(self.create_getter(private_name)))

    def __call__(self) -> List[str]:
        return self.__path

    def to_dict(self) -> dict:
        result = {}

        for name in self.__annotations__:
            if name.startswith("_Node__"):
                continue 

            value = getattr(self, name)
            if isinstance(value, Node):
                value = value.to_dict() 

            key = format_alias(name)
            result[key] = value or None 

        return result

    def create_getter(self, private_prop_name: str) -> Callable:
        def getter(self):
            return nested_getattr(self, [private_prop_name, "_Node__value"])
        return getter

    def to_pydantic(self) -> BaseModel:
        return type(f"Pydantic{self.__class__.__name__}", (BaseModel,), {
            "__annotations__": self.__annotations__
        })(**self.to_dict())

    def from_pydantic(self, pydantic_model: BaseModel) -> Node:
        return type(f"{pydantic_model.__class__.__name__}Node", (Node,), {
            "__annotations__": pydantic_model.__annotations__
        })(**pydantic_model.dict())

    @property
    def class_snake_name(self) -> str:
        return camel_to_snake(self.__class__.__name__)

class Edge:
    source: List[str] 
    sink: List[str]
    serialized: Tuple

    def __init__(self, source: List[str], sink: List[str], function: Callable = None):
        self.source = source
        self.sink = sink
        self.function = function

        self.serialized = (tuple(self.source), tuple(self.sink), self.function and self.function.__name__)

class Event:
    type: TraversalEventEnum
    time: int 
    
    edge: Optional[Edge]
    exception: Optional[Exception]
    state: Optional[dict]

    def __init__(self, type: TraversalEventEnum, **kwargs: Union[Edge, Exception, dict]):
        self.type = type 
        self.time = time_ns() 

        for attr_name in self.__annotations__:
            if not (val := kwargs.get(attr_name)):
                continue 
            setattr(self, attr_name, val)

class Graph:
    edges: List[Edge] 
    outputs: List[str]

    def __init__(self, edges: List[Edge] = [], outputs: List[str] = [], event_handler: Optional[Callable] = None):
        self.edges = edges
        self.outputs = outputs
        self.event_handler = event_handler

    def traverse(self, *args: Union[Node, BaseModel], outputs: List[str] = []) -> dict:
        if outputs:
            subgraph = self.create_subgraph(outputs)
            return subgraph.traverse(*args)

        node_args = [arg if isinstance(arg, Node) else Node().from_pydantic(arg) for arg in args]
        state = {node_arg.class_snake_name: node_arg.to_dict() for node_arg in node_args}

        edges_traversed: Set[Tuple] = set()
        complete = False

        self.trigger_event(TraversalEventEnum.TraversalStarted)

        while not complete:
            complete = True
            flattened_state = flatten(state).items()

            for path, value in flattened_state:
                edges = self.search(source=path, exclude=edges_traversed)

                if not edges:
                    continue
                
                complete = False

                for edge in edges:
                    self.trigger_event(TraversalEventEnum.EdgeStarted, edge=edge)

                    value = get(state, edge.source)
                    
                    if edge.function:
                        if self.search(sink=tuple(edge.source), comparitive_operator=ComparitiveOperationEnum.Intersect, exclude=edges_traversed.union({edge.serialized})):
                            continue
                        
                        input_model = edge.function.__annotations__[edge.source[-1]]
                        input = input_model(**value) if issubclass(input_model, Node) else value
                        try:
                            output = edge.function(input)
                        except Exception as e:
                            if self.trigger_event(TraversalEventEnum.EdgeException, exception=e):
                                output = None
                            else:
                                raise e
                        value = output.to_dict() if isinstance(output, Node) else output

                    set_(state, edge.sink, value)
                    edges_traversed.add(edge.serialized)

                    self.trigger_event(TraversalEventEnum.EdgeEnded, poo="pee")

        self.trigger_event(TraversalEventEnum.TraversalEnded, state=state)

        result = {}
        for name in self.outputs or state:
            data = state.get(name)
            value = model(**data) if (model := globals().get(f"node_{name}")) and data else data
            result[name] = value

        return result

    def search(
        self, 
        source: Tuple[str, ...] = None, 
        sink: Tuple[str, ...] = None, 
        exclude: Set[Tuple] = None, 
        comparitive_operator: ComparitiveOperationEnum = ComparitiveOperationEnum.Equal
    ) -> List[Edge]:

        def compare(path1, path2):
            if comparitive_operator == ComparitiveOperationEnum.Equal:
                return path1 == path2 
            elif comparitive_operator == ComparitiveOperationEnum.Intersect:
                return iterables_intersect(path1, path2)

        def conditions(edge: Edge):
            if exclude and edge.serialized in exclude:
                return False 
            if source and not compare(tuple(edge.source), source):
                return False 
            if sink and not compare(tuple(edge.sink), sink):
                return False 
            return True

        return [edge for edge in self.edges if conditions(edge)]

    def create_subgraph(self, outputs: List[str]) -> Graph:
        frontier: List[Edge] = sum([self.search(sink=(output,), comparitive_operator=ComparitiveOperationEnum.Intersect) for output in outputs], [])
        edges_serialized = set()
        edges = []

        while frontier:
            for edge in frontier:
                edges_serialized.add(edge.serialized)
            
            edges += frontier
            frontier = sum([self.search(sink=tuple(fr_edge.source), comparitive_operator=ComparitiveOperationEnum.Equal, exclude=edges_serialized) for fr_edge in frontier], [])

        return self.__class__(edges=list(edges), outputs=outputs, event_handler=self.event_handler)

    def trigger_event(self, event_type: TraversalEventEnum, **kwargs):
        event = Event(event_type, **kwargs)

        if handler := self.event_handler:
            handler(event)
            return True
        else:
            return False

class GraphFactory:
    default_event_handler: Optional[Callable] 

    def __init__(self, event_handler: Optional[Callable] = None):
        self.default_event_handler = event_handler

    def create(self, edges: List[Edge], event_handler: Optional[Callable] = None):
        return Graph(edges, event_handler=(event_handler or self.default_event_handler))
