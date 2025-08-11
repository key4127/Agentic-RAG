import os
from pathlib import Path
from llama_index.core import Settings
from llama_index.core.llms import MockLLM
from backend.core.loading.document_loader import load_document
from backend.core.loading.document_splitter import split_document
from backend.core.embedding.embedding_model import EmbeddingModel

DATA_DIR = Path("docs")

Settings.llm = MockLLM()

def process_job():
    processed_nodes = []

    embedding_model = EmbeddingModel("local:BAAI/bge-m3")

    with os.scandir(DATA_DIR) as entries: 
        for entry in entries:
            if entry.is_dir():
                for file in os.listdir(entry.path):
                    file_path = Path(entry.path) / file
                    if file_path.suffix == '.md' and not file_path.name.endswith('.en.md'):
                        document = load_document(file_path)
                        origin_nodes = split_document(document)
                        embedded_nodes = embedding_model.embed(origin_nodes)
                        processed_nodes.extend(embedded_nodes)

if __name__ == "__main__":
    process_job()