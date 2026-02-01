from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LearningPlanModel, UserProfileModel
from app.schemas import (
    LearningPlan,
    LessonUnit,
    UserProfile,
    UserProfileInput,
)
from app.services.llm import llm_service


class ProfilingAgent:
    """
    用户画像 Agent

    功能：
    - 接收用户的阶段、方向、计划、目标、节奏等原始输入
    - 调用 LLM 生成结构化的用户画像摘要
    - 将画像写入数据库，作为长期记忆
    """

    async def create_or_update_profile(
        self, db: AsyncSession, raw: UserProfileInput
    ) -> UserProfile:
        system_prompt = (
            "你是一个学习规划专家，请根据用户的学习阶段、方向、计划、目标、节奏，"
            "用简洁的中文总结出：用户优势、薄弱点、学习偏好、潜在风险点。"
            "输出时使用结构化的段落，方便后续被机器解析。"
        )
        content = (
            f"学习阶段: {raw.stage}\n"
            f"学习方向: {raw.direction}\n"
            f"学习计划: {raw.plan}\n"
            f"学习目标: {raw.goal}\n"
            f"学习节奏: {raw.pace}\n"
        )
        summary = await llm_service.summarize(content, system_prompt)

        # 简化处理：这里只保存 summary，其余结构化字段先留空，后续可以做二次解析。
        now = datetime.utcnow()
        model = UserProfileModel(
            summary=summary,
            strengths=[],
            weaknesses=[],
            preferences=[],
            risk_points=[],
            created_at=now,
            updated_at=now,
        )
        db.add(model)
        await db.commit()
        await db.refresh(model)

        return UserProfile(
            id=model.id,
            summary=model.summary,
            strengths=[],
            weaknesses=[],
            preferences=[],
            risk_points=[],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


profiling_agent = ProfilingAgent()

