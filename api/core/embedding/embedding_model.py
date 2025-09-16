from typing import List
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.schema import BaseNode

class EmbeddingModel:
    def __init__(self, model_name: str):
        self.embed_model = resolve_embed_model(model_name)

    def get_embedding_model(self):
        return self.embed_model

    def embed(self, nodes: List[BaseNode]) -> List[BaseNode]:
        texts = [node.get_content() for node in nodes]
        embeddings = self.embed_model.get_text_embedding_batch(texts)

        for i, node in enumerate(nodes):
            node.embedding = embeddings[i]
            
        return nodes