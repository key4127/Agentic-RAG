import os
from pathlib import Path
from llama_index.core.schema import Document

def load_document(path: Path) -> Document:
    """
    Load a document from a file.
    """

    with open(path, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        remaining_content = file.read()

    content = first_line + "\n" + remaining_content
    return Document(
        text=content,
        metadata={
            "category": path.parent.name,
            "number": path.stem,
            "title": first_line.lstrip('#').strip()
        }
    )