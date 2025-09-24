from llama_index.llms.deepseek import DeepSeek
from api.services.agent.course_agent import CourseAgent
from api.dependencies import get_vector_tool
from api.dependencies import get_web_tool
import asyncio
import os


origin_vector_tool = get_vector_tool()
origin_web_tool = get_web_tool()
tool = ""


class vector_tool:

    async def query(query: str):
        """
        This is a tool function to retrieve docs that are related to queries.
        Docs contains information about many famous courses \ 
        for self learning computer science.
        """
        global tool
        tool = "vector"
        return await origin_vector_tool.query(query)


class web_tool:

    async def query(query: str):
        """
        This is a tool function to search on the Internet.
        """
        global tool
        tool = "web"
        return await origin_web_tool.query(query)


async def main():
    input_file = "./data/agent.txt"

    llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
    agent = CourseAgent(
        llm,
        vector_tool,
        web_tool
    )

    skip_tests = 0
    tested_lines = 0
    correct_num = 0
    n = 0

    try:
        with open(input_file, "r", encoding="utf-8") as input:
            lines = input.readlines()
            n = len(lines)

            for i in range(n // 2):
                if i >= skip_tests:
                    global tool
                    tool = ""

                    q = lines[2 * i]
                    a = lines[2 * i + 1]
                    a = a[:-1]

                    await agent.query(q)

                    if tool != "vector" and tool != "web":
                        tool = "self"

                    if tool == a:
                        correct_num += 1
                    
                    tested_lines += 2
    except Exception:
        print(f'{tested_lines // 2} tests finished')
        print(f'{correct_num} tests passed')

    print(f'{tested_lines // 2} tests finished')
    print(f'{correct_num} tests passed')
    print(f'{skip_tests + tested_lines // 2} tests passed totally')
    print(f'result: {correct_num / n * 2}')


if __name__ == "__main__":
    asyncio.run(main())