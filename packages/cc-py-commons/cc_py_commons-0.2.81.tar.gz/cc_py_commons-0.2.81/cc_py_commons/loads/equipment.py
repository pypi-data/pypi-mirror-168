import uuid
from dataclasses import dataclass

@dataclass
class Equipment:

    id: uuid.UUID
    name: str
    active: bool
