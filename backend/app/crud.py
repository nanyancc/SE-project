import json
from datetime import datetime
from typing import Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import and_, case, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import Select

from .config import get_settings
from .models import (
    ArchiveDoc,
    DeclarationNotice,
    GraduationScore,
    MidtermCheck,
    OpeningReport,
    ThesisTopic,
    SysUser,  # 新增
    TopicSelection,  # 新增
)
from .schemas import (
    ArchiveDocCreate,
    ArchiveDocUpdate,
    MidtermCheckCreate,
    MidtermCheckUpdate,
    NoticeCreate,
    NoticeUpdate,
    OpeningReportCreate,
    OpeningReportUpdate,
    ScoreCreate,
    ScoreUpdate,
    StatsResponse,
    TopicCreate,
    TopicUpdate,
    TopicSelectionCreate,  # 新增
    calc_score_level,
    calc_total_score,
)

settings = get_settings()
TEST_USER_ID = settings.test_user_id


# --- 新增：初始化测试用户，防止外键报错 ---
async def ensure_test_users(session: AsyncSession):
    """
    检查 SysUser 表中是否存在 ID=TEST_USER_ID 的用户。
    如果不存在，则创建一个，用于开发测试。
    """
    stmt = select(SysUser).where(SysUser.id == TEST_USER_ID)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        # 创建一个测试用户，身兼多职
        test_user = SysUser(
            id=TEST_USER_ID,
            user_code="TEST001",
            user_name="测试用户(师生同体)",
            user_role="Student",  # 简单起见，角色可以混用，或者你需要在业务层区分
        )
        session.add(test_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            # 可能并发创建了，忽略
            pass


def _total_expr():
    # Prefer stored TOTAL_SCORE; fallback to calculated value if NULL.
    return func.coalesce(
        GraduationScore.total_score,
        (
            (func.coalesce(GraduationScore.process_score, 0) * 0.2)
            + (func.coalesce(GraduationScore.opening_score, 0) * 0.1)
            + (func.coalesce(GraduationScore.midterm_score, 0) * 0.1)
            + (func.coalesce(GraduationScore.thesis_score, 0) * 0.3)
            + (func.coalesce(GraduationScore.defense_score, 0) * 0.3)
        ),
    )


def _build_conditions(
    student_id: Optional[int],
    topic_id: Optional[int],
    score_range: Optional[str],
    level: Optional[str],
    published: Optional[int],
):
    conditions = []
    if student_id is not None:
        conditions.append(GraduationScore.student_id == student_id)
    if topic_id is not None:
        conditions.append(GraduationScore.topic_id == topic_id)
    total_expr = _total_expr()
    if score_range:
        try:
            min_score, max_score = (part.strip() for part in score_range.split("-", 1))
            conditions.append(total_expr.between(float(min_score), float(max_score)))
        except ValueError:
            pass
    if level:
        conditions.append(GraduationScore.score_level == level)
    if published is not None:
        conditions.append(GraduationScore.is_published == published)
    return conditions


def _apply_total_and_level(data: dict) -> dict:
    sub_scores = (
        "process_score",
        "opening_score",
        "midterm_score",
        "thesis_score",
        "defense_score",
    )
    if any(k in data for k in sub_scores):
        total = calc_total_score(
            data.get("process_score"),
            data.get("opening_score"),
            data.get("midterm_score"),
            data.get("thesis_score"),
            data.get("defense_score"),
        )
        data["total_score"] = round(total, 2)
        data["score_level"] = calc_score_level(total)
    return data


async def list_scores(
    session: AsyncSession,
    student_id: Optional[int],
    topic_id: Optional[int],
    score_range: Optional[str],
    level: Optional[str],
    published: Optional[int],
    limit: int,
    offset: int,
) -> Tuple[list[GraduationScore], int]:
    conditions = _build_conditions(student_id, topic_id, score_range, level, published)
    base_stmt: Select = select(GraduationScore)
    if conditions:
        base_stmt = base_stmt.where(and_(*conditions))
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = (await session.execute(count_stmt)).scalar_one()
    data_stmt = (
        base_stmt.order_by(GraduationScore.id.desc()).limit(limit).offset(offset)
    )
    result = await session.execute(data_stmt)
    return result.scalars().all(), total


async def create_score(session: AsyncSession, payload: ScoreCreate) -> GraduationScore:
    data = _apply_total_and_level(payload.model_dump())
    db_obj = GraduationScore(**data)
    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail="学生ID或课题ID不存在") from exc


async def update_score(
    session: AsyncSession, score_id: int, payload: ScoreUpdate
) -> Optional[GraduationScore]:
    db_obj = await session.get(GraduationScore, score_id)
    if not db_obj:
        return None
    updates = _apply_total_and_level(payload.model_dump(exclude_unset=True))
    for field, value in updates.items():
        setattr(db_obj, field, value)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def batch_update_status(
    session: AsyncSession, ids: list[int], is_published: int
) -> int:
    stmt = (
        update(GraduationScore)
        .where(GraduationScore.id.in_(ids))
        .values(is_published=is_published)
        .execution_options(synchronize_session="fetch")
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount or 0


async def get_stats(
    session: AsyncSession,
    student_id: Optional[int],
    topic_id: Optional[int],
    score_range: Optional[str],
    level: Optional[str],
    published: Optional[int],
) -> StatsResponse:
    conditions = _build_conditions(student_id, topic_id, score_range, level, published)
    total_expr = _total_expr()
    agg_stmt = select(
        func.count().label("count"),
        func.avg(total_expr).label("avg"),
        func.max(total_expr).label("max"),
        func.min(total_expr).label("min"),
        func.sum(case((total_expr >= 60, 1), else_=0)).label("pass_count"),
        func.sum(case((total_expr >= 90, 1), else_=0)).label("excellent_count"),
    ).select_from(GraduationScore)
    if conditions:
        agg_stmt = agg_stmt.where(and_(*conditions))
    row = (await session.execute(agg_stmt)).one()
    count = row.count or 0
    if not count:
        return StatsResponse(
            count=0, avg=0, max=0, min=0, pass_rate=0, excellent_rate=0
        )
    pass_rate = (row.pass_count or 0) / count
    excellent_rate = (row.excellent_count or 0) / count
    return StatsResponse(
        count=count,
        avg=float(row.avg or 0),
        max=float(row.max or 0),
        min=float(row.min or 0),
        pass_rate=pass_rate,
        excellent_rate=excellent_rate,
    )


# ---------- DECLARATION_NOTICE ----------
def _notice_type_to_code(label: str) -> str:
    return "1" if label == "初次申报" else "2"


def _notice_code_to_label(code: str) -> str:
    return "初次申报" if code == "1" else "二次补申报"


def _notice_status(notice: DeclarationNotice) -> str:
    if notice.is_deleted:
        return "已撤回"
    if notice.publish_time:
        return "已发布"
    return "草稿"


def _parse_notice_content(content: str | None) -> dict:
    if not content:
        return {}
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"requirement": content}


def _pack_notice_content(payload: NoticeCreate | NoticeUpdate) -> str:
    data = {
        "requirement": payload.requirement,
        "majors": payload.majors,
        "teacher_scope": payload.teacher_scope,
        "auto_remind": payload.auto_remind,
    }
    return json.dumps(data, ensure_ascii=False)


async def list_notices(
    session: AsyncSession,
    keyword: Optional[str],
    type_label: Optional[str],
    status: Optional[str],
) -> list[DeclarationNotice]:
    stmt: Select = select(DeclarationNotice).order_by(DeclarationNotice.id.desc())
    conditions = []
    if keyword:
        like_kw = f"%{keyword}%"
        conditions.append(
            or_(
                DeclarationNotice.title.like(like_kw),
                DeclarationNotice.content.like(like_kw),
            )
        )
    if type_label:
        conditions.append(
            DeclarationNotice.declare_type == _notice_type_to_code(type_label)
        )
    if status == "已发布":
        conditions.append(DeclarationNotice.is_deleted == 0)
        conditions.append(DeclarationNotice.publish_time.isnot(None))
    elif status == "草稿":
        conditions.append(DeclarationNotice.publish_time.is_(None))
        conditions.append(DeclarationNotice.is_deleted == 0)
    elif status == "已撤回":
        conditions.append(DeclarationNotice.is_deleted == 1)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    res = await session.execute(stmt)
    return res.scalars().all()


async def create_notice(
    session: AsyncSession, payload: NoticeCreate
) -> DeclarationNotice:
    data = payload.model_dump()
    declare_type = _notice_type_to_code(payload.type)
    publish_time = None
    is_deleted = 0
    if payload.status == "已发布":
        publish_time = datetime.utcnow()
    elif payload.status == "已撤回":
        is_deleted = 1
    db_obj = DeclarationNotice(
        title=payload.title,
        declare_type=declare_type,
        start_time=payload.start_time,
        end_time=payload.end_time,
        publisher=payload.publisher,
        publish_time=publish_time,
        is_deleted=is_deleted,
        content=_pack_notice_content(payload),
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_notice(
    session: AsyncSession, notice_id: int, payload: NoticeUpdate
) -> Optional[DeclarationNotice]:
    db_obj = await session.get(DeclarationNotice, notice_id)
    if not db_obj:
        return None
    db_obj.title = payload.title
    db_obj.declare_type = _notice_type_to_code(payload.type)
    db_obj.start_time = payload.start_time
    db_obj.end_time = payload.end_time
    db_obj.publisher = payload.publisher or db_obj.publisher
    db_obj.content = _pack_notice_content(payload)
    if payload.status == "已发布":
        db_obj.publish_time = datetime.utcnow()
        db_obj.is_deleted = 0
    elif payload.status == "已撤回":
        db_obj.is_deleted = 1
    else:
        # 草稿状态：保持 publish_time 不变（数据库不允许 NULL）
        db_obj.is_deleted = 0
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def publish_notice(session: AsyncSession, notice_id: int) -> Optional[int]:
    stmt = (
        update(DeclarationNotice)
        .where(DeclarationNotice.id == notice_id)
        .values(publish_time=func.now(), is_deleted=0)
    )
    res = await session.execute(stmt)
    await session.commit()
    return res.rowcount or 0


async def revoke_notice(session: AsyncSession, notice_id: int) -> Optional[int]:
    stmt = (
        update(DeclarationNotice)
        .where(DeclarationNotice.id == notice_id)
        .values(is_deleted=1)
    )
    res = await session.execute(stmt)
    await session.commit()
    return res.rowcount or 0


# ---------- THESIS_TOPIC ----------
async def list_topics(
    session: AsyncSession,
    keyword: Optional[str],
    topic_type: Optional[str],
    audit_status: Optional[str],
    publish_status: Optional[int],
    teacher_id: Optional[int],
    limit: int,
    offset: int,
) -> Tuple[list[ThesisTopic], int]:
    stmt: Select = select(ThesisTopic).order_by(ThesisTopic.id.desc())
    conditions = []
    if keyword:
        like_kw = f"%{keyword}%"
        conditions.append(ThesisTopic.topic_name.like(like_kw))
    if topic_type:
        conditions.append(ThesisTopic.topic_type == topic_type)
    if audit_status:
        conditions.append(ThesisTopic.audit_status == audit_status)
    if publish_status is not None:
        conditions.append(ThesisTopic.publish_status == publish_status)
    # 强制映射到测试用户
    conditions.append(ThesisTopic.teacher_id == TEST_USER_ID)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar_one()
    res = await session.execute(stmt.limit(limit).offset(offset))
    return res.scalars().all(), total


async def create_topic(session: AsyncSession, payload: TopicCreate) -> ThesisTopic:
    data = payload.model_dump()
    data["teacher_id"] = TEST_USER_ID
    db_obj = ThesisTopic(**data)
    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Teacher ID 不存在") from exc


async def update_topic(
    session: AsyncSession, topic_id: int, payload: TopicUpdate
) -> Optional[ThesisTopic]:
    db_obj = await session.get(ThesisTopic, topic_id)
    if not db_obj:
        return None
    updates = payload.model_dump(exclude_unset=True)
    updates.pop("teacher_id", None)
    for field, value in updates.items():
        setattr(db_obj, field, value)
    db_obj.teacher_id = TEST_USER_ID
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


# ---------- STUDENTS ----------
async def list_students(session: AsyncSession, keyword: Optional[str]) -> list[dict]:
    selection_subq = (
        select(
            TopicSelection.student_id.label("student_id"),
            TopicSelection.topic_id.label("topic_id"),
        )
        .where(TopicSelection.volunteer_order == 1)
        .subquery()
    )
    topic_id_expr = func.coalesce(OpeningReport.topic_id, selection_subq.c.topic_id)

    stmt = (
        select(
            SysUser.id.label("id"),
            SysUser.user_code.label("user_code"),
            SysUser.user_name.label("user_name"),
            SysUser.user_role.label("user_role"),
            topic_id_expr.label("topic_id"),
            ThesisTopic.topic_name.label("topic_name"),
            MidtermCheck.id.label("midterm_id"),
            MidtermCheck.check_result.label("check_result"),
        )
        .select_from(SysUser)
        .outerjoin(OpeningReport, OpeningReport.student_id == SysUser.id)
        .outerjoin(selection_subq, selection_subq.c.student_id == SysUser.id)
        .outerjoin(ThesisTopic, ThesisTopic.id == topic_id_expr)
        .outerjoin(MidtermCheck, MidtermCheck.student_id == SysUser.id)
        .where(SysUser.user_role.in_(["Student", "学生", "STUDENT"]))
        .order_by(SysUser.id.asc())
    )
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(
            or_(
                SysUser.user_name.like(like),
                SysUser.user_code.like(like),
            )
        )

    res = await session.execute(stmt)
    items = []
    for row in res.all():
        status = "未提交"
        if row.midterm_id is not None:
            status = row.check_result or "已提交"
        display_name = row.user_name or row.user_code or str(row.id)
        items.append(
            {
                "id": row.id,
                "name": display_name,
                "user_code": row.user_code,
                "user_role": row.user_role,
                "topic_id": row.topic_id,
                "topic_name": row.topic_name,
                "status": status,
            }
        )
    return items


# ---------- TOPIC_SELECTION (NEW) ----------
async def list_my_selections(session: AsyncSession) -> list[TopicSelection]:
    stmt = (
        select(TopicSelection)
        .where(TopicSelection.student_id == TEST_USER_ID)
        .order_by(TopicSelection.volunteer_order)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_selection(
    session: AsyncSession, payload: TopicSelectionCreate
) -> TopicSelection:
    # 检查是否重复选题 (同志愿位置)
    stmt = select(TopicSelection).where(
        TopicSelection.student_id == TEST_USER_ID,
        TopicSelection.volunteer_order == payload.volunteer_order,
    )
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, detail=f"志愿顺序 {payload.volunteer_order} 已存在"
        )

    db_obj = TopicSelection(
        student_id=TEST_USER_ID,
        topic_id=payload.topic_id,
        volunteer_order=payload.volunteer_order,
        select_status="待确认",
    )
    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="所选课题ID不存在")
    return db_obj


# ---------- ARCHIVE_DOC ----------
async def list_archive_docs(
    session: AsyncSession, student_id: Optional[int]
) -> list[ArchiveDoc]:
    stmt: Select = select(ArchiveDoc).order_by(ArchiveDoc.id.desc())
    # 强制映射到测试用户
    stmt = stmt.where(ArchiveDoc.student_id == TEST_USER_ID)
    res = await session.execute(stmt)
    return res.scalars().all()


async def create_archive_doc(
    session: AsyncSession, payload: ArchiveDocCreate
) -> ArchiveDoc:
    data = payload.model_dump()
    data["student_id"] = TEST_USER_ID
    db_obj = ArchiveDoc(**data)
    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail="学生ID不存在") from exc


async def update_archive_doc(
    session: AsyncSession, doc_id: int, payload: ArchiveDocUpdate
) -> Optional[ArchiveDoc]:
    db_obj = await session.get(ArchiveDoc, doc_id)
    if not db_obj:
        return None
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_obj, field, value)
    db_obj.student_id = TEST_USER_ID
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


# ---------- MIDTERM_CHECK ----------
async def get_midterm_by_student(
    session: AsyncSession, student_id: int
) -> Optional[MidtermCheck]:
    # 使用传入的 student_id 查询，而不是 TEST_USER_ID
    stmt = select(MidtermCheck).where(MidtermCheck.student_id == student_id)
    res = await session.execute(stmt)
    return res.scalars().first()


async def upsert_midterm(
    session: AsyncSession, payload: MidtermCheckCreate
) -> MidtermCheck:
    try:
        # 使用 payload 中的 student_id
        actual_student_id = payload.student_id
        existing = await get_midterm_by_student(session, actual_student_id)
        if existing:
            for field, value in payload.model_dump(exclude_unset=True).items():
                if field != "student_id":  # 不更新 student_id
                    setattr(existing, field, value)
            session.add(existing)
            await session.commit()
            await session.refresh(existing)
            return existing
        # 直接使用 payload 中的数据创建，包括正确的 student_id
        db_obj = MidtermCheck(**payload.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        await session.rollback()
        # Likely student_id not found in SYS_USER (FK constraint)
        raise HTTPException(
            status_code=400,
            detail="学生不存在，无法保存中期检查记录",
        ) from exc


async def update_midterm(
    session: AsyncSession, check_id: int, payload: MidtermCheckUpdate
) -> Optional[MidtermCheck]:
    db_obj = await session.get(MidtermCheck, check_id)
    if not db_obj:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)
    # 不再强制覆盖 student_id
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


# ---------- OPENING_REPORT ----------
async def get_opening_by_student(
    session: AsyncSession, student_id: int
) -> Optional[OpeningReport]:
    stmt = select(OpeningReport).where(OpeningReport.student_id == student_id)
    res = await session.execute(stmt)
    return res.scalars().first()


async def create_opening_report(
    session: AsyncSession, payload: OpeningReportCreate
) -> OpeningReport:
    data = payload.model_dump()

    # ❌ 必须删除下面这一行！否则无论谁提交，都变成测试用户(ID=1)的报告
    # data["student_id"] = TEST_USER_ID

    # ✅ 正确：直接使用 payload 里包含的 student_id
    db_obj = OpeningReport(**data)

    session.add(db_obj)
    try:
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except IntegrityError as exc:
        await session.rollback()
        # 这里的提示也顺便改得更准确一点
        raise HTTPException(
            status_code=400, detail="提交失败：该学生可能已存在开题报告，或课题ID无效"
        ) from exc


async def update_opening_report(
    session: AsyncSession, report_id: int, payload: OpeningReportUpdate
) -> Optional[OpeningReport]:
    db_obj = await session.get(OpeningReport, report_id)
    if not db_obj:
        return None

    # 自动更新 payload 里传来的字段
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)

    # ❌ 必须删除下面这一行！否则更新报告时，会将归属人强行改为 ID=1
    # db_obj.student_id = TEST_USER_ID

    await session.commit()
    await session.refresh(db_obj)
    return db_obj


# 添加到 crud.py 文件中
async def delete_topic(session: AsyncSession, topic_id: int) -> bool:
    db_obj = await session.get(ThesisTopic, topic_id)
    if not db_obj:
        return False
    await session.delete(db_obj)
    await session.commit()
    return True
