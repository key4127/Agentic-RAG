from api.services.agent.course_agent import CourseAgent

async def query(query: str, agent: CourseAgent):
    print(query)
    response = await agent.query(query)
    return {
        "query": query,
        "answer": str(response)
    }