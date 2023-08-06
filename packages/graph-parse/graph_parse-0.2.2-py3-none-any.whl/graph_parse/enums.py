

from enum import Enum 

class ComparitiveOperationEnum(Enum):
    Equal = "eq"
    Intersect = "intersect"

class TraversalEventEnum(Enum):
    TraversalStarted = "start"
    TraversalEnded = "end"

    EdgeStarted = "edge_start" 
    EdgeEnded = "edge_end"
    EdgeException = "edge_exception"