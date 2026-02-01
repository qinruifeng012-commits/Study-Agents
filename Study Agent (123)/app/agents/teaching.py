from app.schemas import LessonContent, LessonUnit
from app.services.llm import llm_service


class TeachingAgent:
    """
    教学 Agent

    功能：
    - 当用户点开某一章节时，生成对应的教学内容
    - 结构：引入问题 → 引导思考 → 核心讲解 → 示例 → 练习题
    - 注意：教学阶段才允许使用较长 prompt，其余阶段尽量保持短 prompt
    """

    async def generate_lesson(self, unit: LessonUnit, topic: str) -> LessonContent:
        system_prompt = (
            "你是一名善于启发式教学的老师。"
            "请先提出 1-2 个与主题高度相关的问题，引导学生思考，"
            "然后再用分步骤的方式讲解核心概念，最后给出简短示例和 3 道练习题。"
        )
        user_prompt = (
            f"当前课程主题: {topic}\n"
            f"当前章节: {unit.title}\n"
            f"请根据这个章节设计一次小型教学。\n"
        )

        full_text = await llm_service.teach(user_prompt, system_prompt)

        # 简化处理：当前版本直接把 LLM 输出拆为几个大块，
        # 未来可以通过模板或标记进一步结构化。
        introduction = information_head(full_text)
        explanation = full_text
        examples = [full_text]
        exercises: list[str] = []

        return LessonContent(
            unit_id=unit.id,
            introduction=introduction,
            explanation=explanation,
            examples=examples,
            exercises=exercises,
        )


def information_head(text: str, max_chars: int = 600) -> str:
    """
    简单的“长 prompt 内记忆控制”示例：
    - 对非常长的输出，只保留前 max_chars 作为引入部分
    - 后续可以根据需要做更细的结构化切分
    """
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3] + "..."


teaching_agent = TeachingAgent()

