import os
from pathlib import Path
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
from backend.core.loading.document_loader import load_document
from backend.core.loading.document_splitter import split_documents
from backend.core.embedding.embedding_model import EmbeddingModel
from backend.core.storage.weaviate import WeaviateStorage

DATA_DIR = Path("docs")

Settings.llm = MockLLM()

def process_job():
    # os.environ["CUDA_VISIBLE_DEVICES"] = ""
    embedding_model = EmbeddingModel("local:BAAI/bge-m3")
    weaviate_model = WeaviateStorage(
        "Agentic_RAG_Docs", 
        "local:BAAI/bge-m3", 
        "localhost", 
        8081,
        50051
    )

    with os.scandir(DATA_DIR) as entries: 
        for entry in entries:
            if entry.is_dir():
                for file in os.listdir(entry.path):
                    file_path = Path(entry.path) / file
                    if file_path.suffix == '.md' and not file_path.name.endswith('.en.md'):
                        document = load_document(file_path)
                        origin_nodes = split_documents(document)
                        embedded_nodes = embedding_model.embed(origin_nodes)
                        weaviate_model.add_nodes(embedded_nodes)

if __name__ == "__main__":
    process_job()