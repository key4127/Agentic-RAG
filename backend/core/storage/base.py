from abc import ABC, abstractmethod
from typing import List
from llama_index.core.schema import BaseNode

class BaseVectorStorage(ABC):

    @abstractmethod
    def add_nodes(self, nodes: List[BaseNode]) -> None:
        pass