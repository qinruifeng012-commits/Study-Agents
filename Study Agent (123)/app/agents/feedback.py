from app.schemas import FeedbackInput, FeedbackResult, UserProfile


class FeedbackAgent:
    """
    反馈 & 调整 Agent

    功能：
    - 根据用户对教学内容、节奏、难度的反馈，分析需要调整的方向
    - 更新用户画像（例如：更偏向图像化/例子驱动/公式推导等）
    - 输出对学习路径调整的摘要，供规划 Agent 使用
    """

    async def analyze_feedback(self, feedback: FeedbackInput) -> FeedbackResult:
        # 当前实现为占位逻辑，主要展示接口形态：
        adjustment_summary = (
            "根据你的评分和评论，我们会在后续章节中：\n"
            "- 略微降低难度，增加更多具体示例；\n"
            "- 在关键知识点前增加一步回顾提示；\n"
            "- 缩短单次课程长度，将复杂内容拆分为多个小节。"
        )

        # 暂不真正修改画像，只返回空的 profile_updates
        return FeedbackResult(profile_updates=None, plan_adjustment_summary=adjustment_summary)


feedback_agent = FeedbackAgent()

