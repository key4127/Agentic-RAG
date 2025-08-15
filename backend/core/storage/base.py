from abc import ABC, abstractmethod
from typing import List
from llama_index.core.schema import BaseNode
from llama_index.core.vector_stores.types import VectorStore

class BaseVectorStorage(ABC):

    @abstractmethod
    def get_vector_store(self) -> VectorStore:
        pass

    @abstractmethod
    def add_nodes(self, nodes: List[BaseNode]) -> None:
        pass