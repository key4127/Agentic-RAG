import os
from openai import OpenAI
from api.services.tool.vector_tool import VectorTool
from api.services.tool.web_tool import WebTool

# class CourseAgent():
#     def __init__(
#         self,
#         llm,
#         vector_tool: VectorTool, 
#         web_tool: WebTool
#     ):
#         self.tools = [
#             vector_tool.query,
#             web_tool.query
#         ]
#         self.agent = FunctionAgent(
#             tools=self.tools,
#             llm=llm,
#             system_prompt="你是一个寻找最合适工具来回答用户问题的助手。你可以选择向量数据库工具、" \
#             "网络搜索工具或不使用任何工具。" \
#             "一旦你决定并调用了一个工具，你必须立即终止整个流程，" \
#             "禁止再调用工具，并将输出直接作为最终结果返回。"
#         )

#     async def query(self, query: str):
#         return await self.agent.run(query)

class CourseAgent():
    def __init__(
        self,
        vector_tool: VectorTool, 
        web_tool: WebTool
    ):
        self.tools = {
            "vector": vector_tool.query,
            "web": web_tool.query
        }
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    async def query(self, query: str):
        vector_response = await self.function_call(
            query,
            "vector"
        )

        response = ""

        if vector_response:
            response = vector_response
            tool = "vector"
        else:
            prompt = "你是一个寻找最合适工具来回答用户问题的助手。现在需要你判定用户的问题是否需要网络搜索。" \
                     "如果这个问题较为简单，不需要网络搜索，你需要直接回答，并返回回答的结果。" \
                     "否则返回web这个单词"
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )
            
            if response.choices and len(response.choices) > 0:
                response = response.choices[0].message.content
            else:
                response = ""

            if response == "web":
                tool = "web"
            else:
                tool = "self"

        if tool == "web":
            web_data = await self.function_call(query, tool)

            prompt = "请基于以下提供的上下文信息来回答问题。如果上下文信息不足，不要编造信息。" \
                     f"{web_data}"
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]

            final_response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False
            )

            if final_response.choices and len(final_response.choices) > 0:
                final_response = final_response.choices[0].message.content
            else:
                final_response = ""
        else:
            final_response = response

        return final_response

    async def function_call(self, query: str, tool_name: str):
        return await self.tools[tool_name](query)