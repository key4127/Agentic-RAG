from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer

class VectorTool:
    def __init__(
        self, 
        retriever: BaseRetriever,
        synthesizer: BaseSynthesizer
    ):
        self.retriever = retriever
        self.synthesizer = synthesizer

    def vector_db_search(self, query: str):
        nodes = self.retriever.retrieve(query)
        print(nodes)
        if not nodes or all(node.score is not None and node.score < 0.5 for node in nodes):
            return ""
        
        response = self.synthesizer.synthesize(query, nodes)
        return response