from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.postprocessor.flashrank_rerank import FlashRankRerank
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.schema import QueryBundle

class VectorTool:
    def __init__(
        self, 
        retriever: BaseRetriever,
        reranker: FlashRankRerank,
        synthesizer: BaseSynthesizer
    ):
        self._retriever = retriever
        self._reranker = reranker
        self._synthesizer = synthesizer

    def vector_db_search(self, query: str):
        nodes = self._retriever.retrieve(query)
        query_bundle = QueryBundle(query)
        filtered_nodes = self._reranker.postprocess_nodes(nodes, query_bundle)

        for node in filtered_nodes:
            print(node.score)

        if not filtered_nodes \
           or all(node.score is not None and node.score < 0.001 for node in filtered_nodes):
            return ""
        
        response = self._synthesizer.synthesize(query, nodes)
        return response