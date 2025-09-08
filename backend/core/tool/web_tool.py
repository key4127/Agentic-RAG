import os
import json
import http.client

class WebTool:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("google.serper.dev")

    async def search_web(self, query: str):
        payload = json.dumps({
            "q": query
        })
        headers = {
            "X-API-KEY": os.environ.get("SERPER_DEV_API_KEY"),
            "Content-Type": "application/json"
        }
        self.conn.request("POST", "/search", payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        return data