import os
from pathlib import Path
from llama_index.core.schema import Document
from llama_index.readers.file import MarkdownReader

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