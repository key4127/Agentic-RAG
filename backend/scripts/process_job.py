import os
from pathlib import Path
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
from llama_index.readers.file import MarkdownReader
from llama_index.core.node_parser import MarkdownNodeParser
from backend.core.loading.document_loader import load_document
from backend.core.loading.document_splitter import split_document
from backend.core.embedding.embedding_model import EmbeddingModel
from backend.core.storage.weaviate import WeaviateStorage

DATA_DIR = Path("docs")

Settings.llm = MockLLM()

def process_job():
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    embedding_model = EmbeddingModel("local:BAAI/bge-m3")
    weaviate_model = WeaviateStorage(
        "Agentic_RAG_Docs", 
        "local:BAAI/bge-m3", 
        "localhost", 
        8081,
        50051
    )

    markdown_reader = MarkdownReader()
    markdown_parser = MarkdownNodeParser()

    with os.scandir(DATA_DIR) as entries: 
        for entry in entries:
            if entry.is_dir():
                for file in os.listdir(entry.path):
                    file_path = Path(entry.path) / file
                    if file_path.suffix == '.md' and not file_path.name.endswith('.en.md'):
                        # document = load_document(file_path)
                        # origin_nodes = split_document(document)
                        documents = markdown_reader.load_data(Path(file_path))
                        origin_nodes = markdown_parser.get_nodes_from_documents(documents)
                        print(origin_nodes)
                        embedded_nodes = embedding_model.embed(origin_nodes)
                        weaviate_model.add_nodes(embedded_nodes)

if __name__ == "__main__":
    process_job()