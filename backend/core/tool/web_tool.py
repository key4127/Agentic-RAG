from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec

class WebTool:
    def __init__(self):
        self._web_tool = DuckDuckGoSearchToolSpec()

    async def search_web(self, query: str):
        try:
            search_result = await self._web_tool.duckduckgo_full_search(
                query,
                "zh-cn"
            )
            return search_result
        except Exception as e:
            print(f'web error: {e}')
            return 'search failed'