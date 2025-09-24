from llama_index.llms.deepseek import DeepSeek
from api.services.agent.course_agent import CourseAgent
from api.dependencies import get_agent
import asyncio


async def main():
    input_file = "./data/agent.txt"

    agent = get_agent()

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

                    q = lines[2 * i]
                    a = lines[2 * i + 1]
                    a = a[:-1]

                    response = await agent.query(q)
                    tool = response["tool"]
                    print(tool)

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