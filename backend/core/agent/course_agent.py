from llama_index.core.agent import ReActAgent
from backend.core.tool.vector_tool import VectorTool
from backend.core.tool.web_tool import WebTool

class CourseAgent():
    def __init__(self, vector_tool: VectorTool, web_tool: WebTool):
        self.tools = {
            "vector_tool": vector_tool,
            "web_tool": web_tool
        }
        self.agent = None

    async def query(self, query: str):
        # return self.tools["vector_tool"].vector_db_search(query)
        return await self.tools["web_tool"].search_web(query)
