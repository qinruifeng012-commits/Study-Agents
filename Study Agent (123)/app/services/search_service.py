from typing import Any, Dict, List


class SearchService:
    """
    统一封装外部检索接口。

    当前仅提供方法签名和伪实现，方便后续对接：
    - Bing Search API
    - Wikipedia API
    - arXiv API
    - YouTube Transcript API
    """

    async def search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        使用 Bing 或其他 Web 搜索引擎检索资料。
        目前返回占位数据，便于联调。
        """
        return [
            {
                "title": "示例搜索结果",
                "url": "https://example.com",
                "snippet": f"这是关于「{query}」的占位搜索结果。",
            }
        ]

    async def search_wikipedia(self, query: str) -> List[Dict[str, Any]]:
        """Wikipedia 摘要检索（占位实现）。"""
        return [
            {
                "title": query,
                "summary": f"Wikipedia 摘要占位内容：{query}",
            }
        ]

    async def search_arxiv(self, query: str) -> List[Dict[str, Any]]:
        """arXiv 论文检索（占位实现）。"""
        return [
            {
                "title": f"arXiv 论文关于 {query}",
                "link": "https://arxiv.org/abs/0000.00000",
                "summary": "这是占位的论文摘要。",
            }
        ]

    async def fetch_youtube_transcript(self, video_id: str) -> str:
        """根据 YouTube 视频 ID 获取字幕文本（占位实现）。"""
        return f"[MOCK TRANSCRIPT] 这是视频 {video_id} 的占位字幕内容。"


search_service = SearchService()

