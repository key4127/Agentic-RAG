from typing import List
from llama_index.core.schema import BaseNode
from .base import BaseVectorStorage
import weaviate
import weaviate.classes.config as wcc
from weaviate.util import generate_uuid5

class WeaviateStorage(BaseVectorStorage):

    def __init__(self, name: str, model: str, host: str, port: int):
        self.model = model
        self.collection_name = name
        self.client = weaviate.connect_to_local(
            host=host,
            port=port
        )

        if not self.client.collections.exists(self.collection_name):
            self.client.collections.create(
                name=self.collection_name,
                properties=[
                    wcc.Property(name="text", data_type=wcc.DataType.TEXT),
                    wcc.Property(name="title", data_type=wcc.DataType.TEXT),
                    wcc.Property(name="number", data_type=wcc.DataType.TEXT),
                    wcc.Property(name="category", data_type=wcc.DataType.TEXT)
                ],
                vectorizer_config=wcc.Configure.Vectorizer.none(),
                vector_index_config=wcc.Configure.VectorIndex.hnsw(
                    distance_metric=wcc.VectorDistances.COSINE
                )
            )

    def add_nodes(self, nodes: List[BaseNode]) -> None:
        my_collection = self.client.collections.get(self.collection_name)

        with my_collection.batch.dynamic() as batch:
            for node in nodes:
                node_string = (f"{node.get_content()}|{node.metadata.get('title', '')}"
                               f"|{node.metadata.get('number', '')}|{node.metadata.get('category', '')}")
                uuid = generate_uuid5(node_string)
                properties = {
                    "text": node.get_content(),
                    "title": node.metadata.get("title", ""),
                    "number": node.metadata.get("number", ""),
                    "category": node.metadata.get("category", "")
                }
                batch.add_object(
                    uuid=uuid,
                    properties=properties,
                    vector=node.embedding
                )