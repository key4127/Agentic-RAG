from llama_index.core.query_engine import BaseQueryEngine

class VectorTool:
    def __init__(self, queryEngine: BaseQueryEngine):
        self.query_engine = queryEngine

    def vector_db_search(self, query: str):
        response = self.query_engine.query(query)
        return response