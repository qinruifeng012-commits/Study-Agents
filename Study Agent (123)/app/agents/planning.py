from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LearningPlanModel
from app.schemas import KnowledgeGraph, LearningPlan, LessonUnit


class PlanningAgent:
    """
    规划 Agent

    功能：
    - 根据知识网和用户画像，生成学习轨迹（单位为章节/单元）
    - 规划结果存入数据库，可复用，避免重复生成
    """

    async def create_plan(
        self,
        db: AsyncSession,
        profile_id: int | None,
        graph: KnowledgeGraph,
    ) -> LearningPlan:
        """
        简化版规划：按知识点拓扑顺序生成章节。
        """
        units: List[LessonUnit] = []
        for order, kp in enumerate(graph.nodes, start=1):
            units.append(
                LessonUnit(
                    id=kp.id,
                    title=kp.name,
                    knowledge_points=[kp.id],
                    estimated_time_minutes=40,
                    order=order,
                )
            )

        summary = f"围绕主题「{graph.topic}」的基础学习计划，共 {len(units)} 个单元。"
        now = datetime.utcnow()
        model = LearningPlanModel(
            profile_id=profile_id,
            topic=graph.topic,
            summary=summary,
            units_json=[unit.model_dump() for unit in units],
            created_at=now,
            updated_at=now,
        )
        db.add(model)
        await db.commit()
        await db.refresh(model)

        return LearningPlan(
            id=model.id,
            profile_id=model.profile_id,
            topic=model.topic,
            summary=model.summary,
            units=units,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


planning_agent = PlanningAgent()

