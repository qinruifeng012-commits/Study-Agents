from typing import List

from app.schemas import KnowledgeGraph, KnowledgePoint


class KnowledgeGraphAgent:
    """
    知识网 Agent

    功能：
    - 基于查询结果（暂不直接接入）构建初步知识网
    - 当前实现：根据主题生成一个非常简单的示例知识网
    - 后续可以接入 LLM/向量库做自动知识点抽取与关系挖掘
    """

    async def build_initial_graph(self, topic: str) -> KnowledgeGraph:
        # 这里先返回一个简单占位的知识网示例
        nodes: List[KnowledgePoint] = [
            KnowledgePoint(
                id="kp_intro",
                name=f"{topic} 基本概念",
                description=f"理解 {topic} 的核心概念与解决的问题。",
                difficulty=1,
                prerequisites=[],
            ),
            KnowledgePoint(
                id="kp_core",
                name=f"{topic} 核心原理",
                description=f"掌握 {topic} 中最核心的思想与关键步骤。",
                difficulty=3,
                prerequisites=["kp_intro"],
            ),
            KnowledgePoint(
                id="kp_advanced",
                name=f"{topic} 进阶应用",
                description=f"将 {topic} 应用于更复杂的场景或项目中。",
                difficulty=4,
                prerequisites=["kp_core"],
            ),
        ]
        return KnowledgeGraph(topic=topic, nodes=nodes)


knowledge_graph_agent = KnowledgeGraphAgent()

