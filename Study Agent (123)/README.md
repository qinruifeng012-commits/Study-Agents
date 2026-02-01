## Study Agent 项目说明

### 项目目标

一个可以**尽量脱离传统教学模式**的 AI 学习助手，让学习更主观、更直接，围绕用户的学习阶段、方向与目标构建个性化的长期学习轨迹。

### 整体架构（逻辑层面）

- **1. 用户画像层（画像 Agent）**
  - 输入：学习阶段、学习方向、学习计划、学习目标、学习节奏等。
  - 由 LLM 总结并生成结构化用户画像，作为**长期记忆**的核心。
- **2. 查询层（查询 Agent）**
  - 基于用户画像和目标，从外部数据源检索相关资料：
    - Bing Search API
    - Wikipedia API
    - arXiv API
    - YouTube Transcript API
  - 将内容做初步清洗与总结，写入向量库。
- **3. 知识网层（知识网 Agent）**
  - 根据查询结果抽取知识点，构建知识框架与知识点之间的联系。
  - 初期使用 JSON Graph 存储，后期可迁移到 Neo4j。
- **4. 规划层（规划 Agent）**
  - 根据用户画像 + 知识网，生成学习轨迹与学习计划（章节、顺序、难度、时间分布）。
  - 规划结果作为**可复用的中间产物**存储，避免重复生成。
- **5. 教学层（教学 Agent）**
  - 当用户点开某一章节时：
    - 先引出问题，激发思考；
    - 再讲解核心知识与解决方案（该章节的核心内容）。
  - 教学阶段才使用**较长的 prompt**，其他阶段尽量短、结构化。
- **6. 复盘层（复盘 Agent）**
  - 教学结束后，分析历史课程：
    - 依据：时间间隔、掌握程度、难度、与当前章节的联系程度；
    - 结合艾宾浩斯遗忘曲线思想，决定是否复习以及复习量。
  - 整合旧知识与新知识，生成练习题与小测验。
- **7. 反馈与自适应层（反馈 & 调整 Agent）**
  - 收集用户反馈（对节奏、内容、形式的评价）和答题表现。
  - 更新用户画像与学习路径，实现持续自适应。

### LLM 层设计

- **教学类任务**：阿里云百炼 `qwen-max`（面向用户的讲解、出题等，长 prompt，最强性能）。
- **总结 / 画像 / 规划 / 知识网**：阿里云百炼 `qwen-turbo`（结构化总结、复用性强，尽量短 prompt，轻量快速）。

通过在代码中抽象出统一的 `LLMService`，使用阿里云百炼 DashScope API 的 OpenAI 兼容接口，便于后续替换模型或接入其他兼容接口。

### 数据层设计

- **用户画像存储**：PostgreSQL / SQLite（当前示例默认 SQLite，便于本地开发）。
- **会话记忆**：Redis（短期对话状态、最近若干轮上下文）。
- **向量搜索**：FAISS / Chroma（本项目骨架先预留接口，具体实现可替换）。
- **知识网存储**：JSON Graph（文件或 JSON 字段），未来可迁移到 Neo4j。

### 查询层

- 统一封装在 `search_service` 中，对上暴露抽象接口，对下适配不同 API：
  - Bing Search API
  - Wikipedia API
  - arXiv API
  - YouTube Transcript API

### 记忆与复用策略（省 token 关键点）

- **知识不重复生成**：知识点与章节内容一旦确认，写入知识网与向量库，下次直接检索和微调补充即可。
- **规划不重复生成**：学习轨迹、章节结构持久化保存，当用户调整需求时以增量方式修改，而不是完全重算。
- **教学才用长 prompt**：教学阶段为了拟人化讲解可以适度使用长 prompt，其余阶段尽量使用结构化、短 prompt。

### 当前代码结构（初始骨架）

- `app/main.py`：FastAPI 入口，定义 HTTP 接口。
- `app/config.py`：基础配置与环境变量。
- `app/schemas.py`：核心 Pydantic 数据模型（用户画像、学习计划、章节、反馈等）。
- `app/agents/`：
  - `profiling.py`：画像 Agent
  - `search.py`：查询 Agent
  - `knowledge_graph.py`：知识网 Agent
  - `planning.py`：规划 Agent
  - `teaching.py`：教学 Agent
  - `review.py`：复盘 Agent
  - `feedback.py`：反馈 & 调整 Agent
- `app/services/`：
  - `llm.py`：LLM 调用封装（阿里云百炼 DashScope API，使用 OpenAI 兼容接口）。
  - `search_service.py`：对外部检索 API 的统一封装。
- `app/db/`：
  - `session.py`：数据库会话与连接管理（默认 SQLite）。
  - `models.py`：SQLAlchemy 模型（用户画像、学习计划等，初始骨架）。

### 运行说明（初版）

1. **创建并激活虚拟环境（推荐）**

   ```bash
   cd "Study Agent (123)"
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**

   在同级目录创建 `.env`（可选）或通过系统环境变量配置：

   - `DASHSCOPE_API_KEY`：阿里云百炼 DashScope API Key（必需）
   - `DASHSCOPE_BASE_URL`：（可选）API 端点地址，默认为北京地域
     - 北京：`https://dashscope.aliyuncs.com/compatible-mode/v1`
     - 新加坡：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
     - 美国：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

4. **启动 API 服务**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **访问文档**

   浏览器打开：`http://127.0.0.1:8000/docs` 查看交互式接口文档。

### 下一步可扩展方向

- 为各个 Agent 实现真实业务逻辑（目前为骨架）。
- 接入真实的外部检索 API 与向量库实现。
- 将知识网从 JSON Graph 迁移到 Neo4j，并增加可视化。
- 加一层前端界面（Web / 桌面）实现完整的学习体验。

