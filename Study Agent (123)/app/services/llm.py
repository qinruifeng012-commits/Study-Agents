from typing import Any, Dict, List, Optional

import httpx

from app.config import get_settings


class LLMService:
    """
    封装 LLM 调用，便于在不同 Agent 中复用。
    使用阿里云百炼 DashScope API（OpenAI 兼容接口）。

    - 教学类任务可使用更强模型（如 qwen-max）
    - 画像 / 总结 / 规划等使用轻量模型（如 qwen-turbo）以节省成本
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.dashscope_api_key
        self.base_url = settings.dashscope_base_url

        # 阿里云百炼模型名称配置
        # qwen-turbo: 轻量快速，适合总结/画像等任务
        # qwen-plus: 平衡性能与成本
        # qwen-max: 最强性能，适合教学等复杂任务
        self.teaching_model = "qwen-max"
        self.summary_model = "qwen-turbo"

    async def _mock_response(self, prompt: str) -> str:
        """当未配置 API key 时，返回可见的占位内容，便于前后端联调。"""
        return f"[MOCK RESPONSE] 当前未配置 DASHSCOPE_API_KEY。\n\nPROMPT 摘要: {prompt[:200]}"

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int | None = None,
    ) -> str:
        """
        通用对话接口，调用阿里云百炼 DashScope API（OpenAI 兼容接口）。

        :param messages: OpenAI Chat 格式的消息列表
        :param model: 可选模型名，默认使用 summary_model
        """
        if not self.api_key:
            # 开发/无 key 场景直接返回 mock
            content = "\n".join(m["content"] for m in messages if m["role"] != "system")
            return await self._mock_response(content)

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": model or self.summary_model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"] or ""

    async def summarize(self, content: str, system_prompt: str) -> str:
        """使用轻量模型做总结/结构化抽取。"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
        return await self.chat(messages, model=self.summary_model)

    async def teach(self, content: str, system_prompt: str) -> str:
        """
        教学专用接口，可以选择更强模型，并允许更长的 prompt。
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
        return await self.chat(messages, model=self.teaching_model, temperature=0.5)


llm_service = LLMService()
