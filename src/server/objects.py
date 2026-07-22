from enum import Enum


class MCServerStatus(Enum):
    OFFLINE = 0
    ONLINE = 1
    STARTING = 2
    STOPPING = 3
