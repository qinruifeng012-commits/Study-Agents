from typing import List

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.feedback import feedback_agent
from app.agents.knowledge_graph import knowledge_graph_agent
from app.agents.planning import planning_agent
from app.agents.profiling import profiling_agent
from app.agents.review import review_agent
from app.agents.search import query_agent
from app.agents.teaching import teaching_agent
from app.config import get_settings
from app.db.models import Base, LearningPlanModel
from app.db.session import engine, get_db
from app.schemas import (
    FeedbackInput,
    FeedbackResult,
    KnowledgeGraph,
    LearningPlan,
    LessonContent,
    LessonRequest,
    ReviewPlan,
    UserProfile,
    UserProfileInput,
)

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug, description="AI学习助手 - 个性化学习轨迹生成系统")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def on_startup() -> None:
    """启动时自动创建数据库表（示例环境用，正式环境建议使用 Alembic 迁移）。"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/", summary="首页")
async def root():
    """返回前端页面"""
    return FileResponse("static/new-index.html")


@app.post("/profile", response_model=UserProfile, summary="创建/更新用户画像")
async def create_profile(
    data: UserProfileInput, db: AsyncSession = Depends(get_db)
) -> UserProfile:
    """创建或更新用户画像，系统会根据输入生成结构化的用户画像"""
    return await profiling_agent.create_or_update_profile(db, data)


@app.get("/search", summary="根据主题检索相关资料")
async def search_resources(topic: str):
    """根据输入的主题，从多个数据源（Bing、Wikipedia、arXiv、YouTube）检索相关学习资料"""
    return await query_agent.search_resources(topic)


@app.post("/knowledge-graph", response_model=KnowledgeGraph, summary="根据主题构建初步知识网")
async def build_knowledge_graph(topic: str) -> KnowledgeGraph:
    """根据输入的主题，构建包含知识点和它们之间关系的知识网络"""
    return await knowledge_graph_agent.build_initial_graph(topic)


@app.post("/plan", response_model=LearningPlan, summary="基于知识网生成学习计划")
async def create_learning_plan(
    topic: str,
    profile_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> LearningPlan:
    """根据用户画像和知识网，生成个性化的学习计划，包括学习章节、顺序和时间安排"""
    graph = await knowledge_graph_agent.build_initial_graph(topic)
    plan = await planning_agent.create_plan(db, profile_id, graph)
    return plan


@app.post("/lesson", response_model=LessonContent, summary="获取某一章节的教学内容")
async def get_lesson(
    req: LessonRequest,
    db: AsyncSession = Depends(get_db),
) -> LessonContent:
    """获取指定章节的教学内容，包括问题引入、核心讲解、示例和练习题"""
    plan: LearningPlanModel | None = await db.get(LearningPlanModel, req.plan_id)
    if not plan:
        raise ValueError("学习计划不存在")

    units_data = plan.units_json or []
    target_unit_data = next((u for u in units_data if u["id"] == req.unit_id), None)
    if not target_unit_data:
        raise ValueError("指定章节不存在")

    unit = LessonContent.model_construct()
    from app.schemas import LessonUnit

    unit_obj = LessonUnit(**target_unit_data)
    return await teaching_agent.generate_lesson(unit_obj, plan.topic)


@app.post("/review", response_model=ReviewPlan, summary="生成复盘/复习计划")
async def get_review_plan(
    req: LessonRequest,
    db: AsyncSession = Depends(get_db),
) -> ReviewPlan:
    """根据当前学习进度和历史记录，生成复习计划，帮助巩固已学知识"""
    from app.schemas import LessonUnit

    plan: LearningPlanModel | None = await db.get(LearningPlanModel, req.plan_id)
    if not plan:
        raise ValueError("学习计划不存在")

    units_data = plan.units_json or []
    units: List[LessonUnit] = [LessonUnit(**u) for u in units_data]
    current = next((u for u in units if u.id == req.unit_id), units[-1])
    history = [u for u in units if u.order < current.order]

    return await review_agent.plan_review(current, history)


@app.post("/feedback", response_model=FeedbackResult, summary="提交教学反馈并获取调整建议")
async def submit_feedback(data: FeedbackInput) -> FeedbackResult:
    """提交学习反馈，系统会分析反馈并调整用户画像和学习路径"""
    return await feedback_agent.analyze_feedback(data)

