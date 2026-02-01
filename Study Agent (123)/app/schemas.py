from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserProfileInput(BaseModel):
    """用户在创建/更新画像时的原始输入。"""

    stage: str = Field(..., description="学习阶段，例如：高中/大学/工作/转行")
    direction: str = Field(..., description="学习方向，例如：前端、算法、物理等")
    plan: str = Field(..., description="大致学习计划描述")
    goal: str = Field(..., description="学习目标，例如：半年内找前端工作")
    pace: str = Field(..., description="学习节奏，例如：每天 2 小时、周末集中学习等")


class UserProfile(BaseModel):
    """LLM 总结后的结构化用户画像（长期记忆核心）。"""

    id: Optional[int] = None
    summary: str = Field(..., description="对用户整体情况的总结")
    strengths: List[str] = Field(default_factory=list, description="用户优势")
    weaknesses: List[str] = Field(default_factory=list, description="薄弱点")
    preferences: List[str] = Field(default_factory=list, description="学习风格偏好")
    risk_points: List[str] = Field(default_factory=list, description="容易放弃或困难的点")
    created_at: datetime
    updated_at: datetime


class KnowledgePoint(BaseModel):
    """知识网中的一个知识点。"""

    id: str
    name: str
    description: str
    difficulty: int = Field(ge=1, le=5, description="难度等级 1-5")
    prerequisites: List[str] = Field(
        default_factory=list, description="前置知识点 ID 列表"
    )


class KnowledgeGraph(BaseModel):
    """知识网整体结构（先以 JSON Graph 形式表示）。"""

    topic: str
    nodes: List[KnowledgePoint]


class LessonUnit(BaseModel):
    """学习计划中的一个章节/单元。"""

    id: str
    title: str
    knowledge_points: List[str] = Field(
        default_factory=list, description="本章节覆盖的知识点 ID 列表"
    )
    estimated_time_minutes: int = 30
    order: int = 0


class LearningPlan(BaseModel):
    """规划 Agent 输出的整体学习轨迹。"""

    id: Optional[int] = None
    profile_id: Optional[int] = None
    topic: str
    summary: str
    units: List[LessonUnit]
    created_at: datetime
    updated_at: datetime


class LessonRequest(BaseModel):
    """请求某一章节教学内容。"""

    plan_id: int
    unit_id: str


class LessonContent(BaseModel):
    """教学 Agent 输出的章节内容。"""

    unit_id: str
    introduction: str = Field(..., description="引入问题与思考")
    explanation: str = Field(..., description="系统讲解与推导")
    examples: List[str] = Field(default_factory=list, description="示例与案例")
    exercises: List[str] = Field(default_factory=list, description="练习题或思考题")


class ReviewItem(BaseModel):
    """需要复习的某一历史知识点或单元。"""

    reference_unit_id: Optional[str] = None
    knowledge_point_id: Optional[str] = None
    reason: str


class ReviewPlan(BaseModel):
    """复盘 Agent 决定的复习计划。"""

    items: List[ReviewItem]
    combined_exercises: List[str] = Field(
        default_factory=list, description="将旧知识与当前章节整合的题目"
    )


class FeedbackInput(BaseModel):
    """用户反馈输入。"""

    profile_id: int
    plan_id: Optional[int] = None
    unit_id: Optional[str] = None
    satisfaction: int = Field(ge=1, le=5, description="整体满意度 1-5")
    difficulty: int = Field(ge=1, le=5, description="主观难度 1-5")
    comment: str = ""
    preferred_changes: List[str] = Field(
        default_factory=list, description="希望如何改进（节奏/难度/形式等）"
    )


class FeedbackResult(BaseModel):
    """反馈分析结果，用于更新用户画像和学习路径。"""

    profile_updates: Optional[UserProfile] = None
    plan_adjustment_summary: Optional[str] = None

