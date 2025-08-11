from typing import List
from llama_index.core.schema import NodeWithScore
from base import BaseVectorStorage

class WeaviateStorage(BaseVectorStorage):

    def __init__(self):
        pass

    def add_nodes(self, nodes: List[NodeWithScore]) -> None:
        for node in nodes:
            pass