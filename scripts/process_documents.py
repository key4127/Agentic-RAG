import os
import weaviate
from pathlib import Path
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
from llama_index.core.schema import Document
from llama_index.readers.file import MarkdownReader
from typing import List
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.schema import Document
from llama_index.core.embeddings import resolve_embed_model
from weaviate.util import generate_uuid5

DATA_DIR = Path("docs")

Settings.llm = MockLLM()

def load_document(path: Path) -> Document:
    """
    Load a document from a file.
    """

    with open(path, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        file.close()
    
    metadata={
        "category": path.parent.name,
        "number": path.stem,
        "title": first_line.lstrip('#').strip()
    }

    return MarkdownReader().load_data(
        path,
        extra_info=metadata
    )

def split_documents(documents: List[Document]) -> List[BaseNode]:
    parser = MarkdownElementNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    return nodes

def add_nodes(client, nodes: List[BaseNode], collection_name) -> None:
        my_collection = client.collections.get(collection_name)

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

def embed(model, nodes: List[BaseNode]) -> List[BaseNode]:
        texts = [node.get_content() for node in nodes]
        embeddings = model.get_text_embedding_batch(texts)

        for i, node in enumerate(nodes):
            node.embedding = embeddings[i]
            
        return nodes

def process_job():
    # os.environ["CUDA_VISIBLE_DEVICES"] = ""
    embedding_model = resolve_embed_model("local:BAAI/bge-m3")
    weaviate_model = weaviate.connect_to_local(
        host="localhost",
        port=8081,
        grpc_port=50051
    )
    collection_name = "Agentic_RAG_Docs"

    with os.scandir(DATA_DIR) as entries: 
        for entry in entries:
            if entry.is_dir():
                for file in os.listdir(entry.path):
                    file_path = Path(entry.path) / file
                    if file_path.suffix == '.md' and not file_path.name.endswith('.en.md'):
                        document = load_document(file_path)
                        origin_nodes = split_documents(document)
                        embedded_nodes = embed(embedding_model, origin_nodes)
                        add_nodes(weaviate_model, embedded_nodes, collection_name)

if __name__ == "__main__":
    process_job()