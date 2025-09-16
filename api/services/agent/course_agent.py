from llama_index.core.agent.workflow import FunctionAgent
from api.services.tool.vector_tool import VectorTool
from api.services.tool.web_tool import WebTool

class CourseAgent():
    def __init__(
        self,
        llm, 
        vector_tool: VectorTool, 
        web_tool: WebTool
    ):
        self.tools = [
            vector_tool.vector_db_search,
            web_tool.search_web
        ]
        self.agent = FunctionAgent(
            tools=self.tools,
            llm=llm,
            system_prompt="你是一个寻找最合适工具来回答用户问题的助手。你可以选择向量数据库工具、" \
            "网络搜索工具或不使用任何工具。" \
            "一旦你决定并调用了一个工具，你必须立即终止整个流程，" \
            "禁止再调用工具，并将输出直接作为最终结果返回。"
        )

    async def query(self, query: str):
        return await self.agent.run(query)