from app.schemas import LessonUnit, ReviewItem, ReviewPlan


class ReviewAgent:
    """
    复盘 Agent

    功能（当前为简化版）：
    - 根据当前章节与历史章节，决定哪些内容需要复习
    - 后续可以加入：时间间隔、掌握程度、难度、联系程度等因素
    """

    async def plan_review(
        self,
        current_unit: LessonUnit,
        history_units: list[LessonUnit],
    ) -> ReviewPlan:
        items: list[ReviewItem] = []

        # 简易策略示例：总是复习最后一个历史单元
        if history_units:
            last_unit = history_units[-1]
            items.append(
                ReviewItem(
                    reference_unit_id=last_unit.id,
                    knowledge_point_id=None,
                    reason=f"与当前章节「{current_unit.title}」联系紧密，需要温习前一章「{last_unit.title}」。",
                )
            )

        return ReviewPlan(items=items, combined_exercises=[])


review_agent = ReviewAgent()

