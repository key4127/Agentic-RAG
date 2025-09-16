from typing import List
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.schema import Document

def split_documents(documents: List[Document]) -> List[BaseNode]:
    parser = MarkdownElementNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    return nodes