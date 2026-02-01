from typing import Any, Dict, List

from app.services.search_service import search_service


class QueryAgent:
    """
    查询 Agent

    功能：
    - 根据用户画像与学习主题，从全网检索相关教程与资料
    - 目前以占位实现为主，后续可对接真实 API 并写入向量库
    """

    async def search_resources(self, topic: str) -> List[Dict[str, Any]]:
        """
        根据主题进行多源检索。
        """
        web_results = await search_service.search_web(topic)
        wiki_results = await search_service.search_wikipedia(topic)
        arxiv_results = await search_service.search_arxiv(topic)

        return [
            {"source": "web", "items": web_results},
            {"source": "wikipedia", "items": wiki_results},
            {"source": "arxiv", "items": arxiv_results},
        ]


query_agent = QueryAgent()

