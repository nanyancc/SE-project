# FastAPI 后端

基于 `FastAPI + SQLAlchemy (async) + MySQL` 的简单成绩服务，路径位于 `./backend`。

## 快速开始
1. 准备虚拟环境并安装依赖
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. 配置环境变量
   ```bash
   cp .env.example .env
   # 按需修改 .env 中的 DB_* 配置连接你的 MySQL
   ```
3. 运行服务
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   默认开放 CORS，前端可通过 `http://localhost:8000/api` 访问。

## 主要接口
- `GET /api/scores`：查询毕业成绩，支持 studentId/topicId/range/level/published 过滤，`limit/offset` 分页。
- `GET /api/scores/stats`：同样的过滤条件下返回 count/avg/max/min/pass_rate/excellent_rate。
- `POST /api/scores`：创建成绩记录（字段见下）。
- `PUT /api/scores/{id}`：更新成绩，自动计算 `total_score` 与 `score_level`（A/B/C/D/F）。
- `POST /api/scores/batch/status`：批量更新发布状态，`{ "ids": [1,2], "is_published": 1 }`。
- 其他表的接口均在 `/api/extra/*`：
- `GET/POST/PUT /api/extra/notices`：课题申报通知（DECLARATION_NOTICE），支持草稿/发布/撤回。
- `GET/POST/PUT /api/extra/topics`：课题信息（THESIS_TOPIC）。
- `GET/POST/PUT /api/extra/archive-docs`：资料归档（ARCHIVE_DOC）。
- `GET/POST/PUT /api/extra/midterm-checks`：中期检查（MIDTERM_CHECK），按 student_id 查询/保存。
- `GET/POST/PUT /api/extra/opening-reports`：开题报告（OPENING_REPORT），按 student_id 查询/保存。

## 测试用户映射
- 配置项 `TEST_USER_ID`（`.env` 的 `TEST_USER_ID`，默认 1），所有涉及用户的写入都强制映射到该测试用户：课题 teacher_id、归档/中期/开题记录 student_id 等。
- 若数据库存在外键约束，请确保 `SYS_USER` 中有该 `TEST_USER_ID`。

## 数据库
- 表结构与需求文档一致：`GRADUATION_SCORE` (SCORE_ID, STUDENT_ID, TOPIC_ID, PROCESS_SCORE, OPENING_SCORE, MIDTERM_SCORE, THESIS_SCORE, DEFENSE_SCORE, TOTAL_SCORE, SCORE_LEVEL, IS_PUBLISHED)。
- 启动时会自动执行一次 `create_all` 以便本地开发初始化表结构；生产建议使用迁移工具（如 Alembic）。
- 计算总评的权重与前端一致：过程 20%、开题 10%、中期 10%、论文 30%、答辩 30%；成绩等级映射 A ≥90, B ≥80, C ≥70, D ≥60，否则 F。
