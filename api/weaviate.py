import weaviate.classes.config as wcc
import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore

class WeaviateStorage():

    def __init__(self, name: str, model: str, host: str, http_port: int, grpc_port: int):
        self.model = model
        self.collection_name = name
        self.client = weaviate.connect_to_local(
            host=host,
            port=http_port,
            grpc_port=grpc_port,
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

    def get_vector_store(self):
        return WeaviateVectorStore(
            weaviate_client=self.client, 
            index_name=self.collection_name
        )

    def close(self) -> None:
        self.client.close()

    def __del__(self):
        self.client.close()