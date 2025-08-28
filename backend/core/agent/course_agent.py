from llama_index.core.agent import ReActAgent
from backend.core.tool.vector_tool import VectorTool

class CourseAgent():
    def __init__(self, vectorTool: VectorTool):
        self.tools = {
            "vector_tool": vectorTool
        }
        self.agent = None

    def query(self, query: str):
        return self.tools["vector_tool"].vector_db_search(query)
