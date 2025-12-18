from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .crud import (
    _notice_code_to_label,
    _notice_status,
    _parse_notice_content,
)
from .database import get_session
from .models import DeclarationNotice
from .schemas import (
    ArchiveDocCreate,
    ArchiveDocOut,
    ArchiveDocUpdate,
    MidtermCheckCreate,
    MidtermCheckOut,
    MidtermCheckUpdate,
    NoticeCreate,
    NoticeOut,
    NoticeUpdate,
    OpeningReportCreate,
    OpeningReportOut,
    OpeningReportUpdate,
    TopicCreate,
    TopicOut,
    TopicUpdate,
    TopicSelectionCreate, # 新增
    TopicSelectionOut,    # 新增
)

router = APIRouter(prefix="/extra", tags=["extra"])


def _notice_to_out(item: DeclarationNotice) -> NoticeOut:
    content = _parse_notice_content(item.content)
    return NoticeOut(
        id=item.id,
        title=item.title,
        type=_notice_code_to_label(item.declare_type),
        declare_type=item.declare_type,
        start_time=item.start_time,
        end_time=item.end_time,
        majors=content.get("majors", []),
        teacher_scope=content.get("teacher_scope", ""),
        requirement=content.get("requirement", ""),
        auto_remind=bool(content.get("auto_remind", False)),
        status=_notice_status(item),
        publisher=item.publisher,
        publish_time=item.publish_time,
        is_deleted=item.is_deleted,
    )


# ---------- Notice ----------
@router.get("/notices", response_model=list[NoticeOut])
async def list_notices(
    keyword: str | None = Query(None),
    type: str | None = Query(None, alias="type"),
    status: str | None = Query(None),
    session: AsyncSession = Depends(get_session),
):
    items = await crud.list_notices(session, keyword, type, status)
    return [_notice_to_out(i) for i in items]


@router.post("/notices", response_model=NoticeOut, status_code=201)
async def create_notice(
    payload: NoticeCreate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.create_notice(session, payload)
    return _notice_to_out(db_obj)


@router.put("/notices/{notice_id}", response_model=NoticeOut)
async def update_notice(
    notice_id: int, payload: NoticeUpdate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.update_notice(session, notice_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Notice not found")
    return _notice_to_out(db_obj)


@router.post("/notices/{notice_id}/publish")
async def publish_notice(notice_id: int, session: AsyncSession = Depends(get_session)):
    updated = await crud.publish_notice(session, notice_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"updated": updated}


@router.post("/notices/{notice_id}/revoke")
async def revoke_notice(notice_id: int, session: AsyncSession = Depends(get_session)):
    updated = await crud.revoke_notice(session, notice_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"updated": updated}


# ---------- Topics ----------
@router.get("/topics")
async def list_topics(
    keyword: str | None = Query(None),
    topic_type: str | None = Query(None, alias="type"),
    audit_status: str | None = Query(None, alias="status"),
    publish_status: int | None = Query(None, alias="publishStatus"),
    teacher_id: int | None = Query(None, alias="teacherId"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    items, total = await crud.list_topics(
        session, keyword, topic_type, audit_status, publish_status, teacher_id, limit, offset
    )
    return {
        "items": [
            TopicOut.model_validate(i)
            for i in items
        ],
        "total": total,
    }


@router.post("/topics", response_model=TopicOut, status_code=201)
async def create_topic(
    payload: TopicCreate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.create_topic(session, payload)
    return db_obj


@router.put("/topics/{topic_id}", response_model=TopicOut)
async def update_topic(
    topic_id: int, payload: TopicUpdate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.update_topic(session, topic_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_obj


# ---------- Selections (NEW) ----------
@router.get("/selections", response_model=list[TopicSelectionOut])
async def list_selections(
    session: AsyncSession = Depends(get_session),
):
    items = await crud.list_my_selections(session)
    return items

@router.post("/selections", response_model=TopicSelectionOut, status_code=201)
async def create_selection(
    payload: TopicSelectionCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_selection(session, payload)


# ---------- Archive Docs ----------
@router.get("/archive-docs", response_model=list[ArchiveDocOut])
async def list_archive_docs(
    student_id: int | None = Query(None, alias="studentId"),
    session: AsyncSession = Depends(get_session),
):
    items = await crud.list_archive_docs(session, student_id)
    return [ArchiveDocOut.model_validate(i) for i in items]


@router.post("/archive-docs", response_model=ArchiveDocOut, status_code=201)
async def create_archive_doc(
    payload: ArchiveDocCreate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.create_archive_doc(session, payload)
    return db_obj


@router.put("/archive-docs/{doc_id}", response_model=ArchiveDocOut)
async def update_archive_doc(
    doc_id: int, payload: ArchiveDocUpdate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.update_archive_doc(session, doc_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Archive doc not found")
    return db_obj


# ---------- Midterm Check ----------
@router.get("/midterm-checks/{student_id}", response_model=MidtermCheckOut)
async def get_midterm(
    student_id: int, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.get_midterm_by_student(session, student_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_obj


@router.post("/midterm-checks", response_model=MidtermCheckOut, status_code=201)
async def upsert_midterm(
    payload: MidtermCheckCreate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.upsert_midterm(session, payload)
    return db_obj


@router.put("/midterm-checks/{check_id}", response_model=MidtermCheckOut)
async def update_midterm(
    check_id: int, payload: MidtermCheckUpdate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.update_midterm(session, check_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_obj


# ---------- Opening Report ----------
@router.get("/opening-reports", response_model=OpeningReportOut | None)
async def get_opening_report(
    student_id: int = Query(..., alias="studentId"),
    session: AsyncSession = Depends(get_session),
):
    db_obj = await crud.get_opening_by_student(session, student_id)
    if not db_obj:
        return None
    return db_obj


@router.post("/opening-reports", response_model=OpeningReportOut, status_code=201)
async def create_opening_report(
    payload: OpeningReportCreate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.create_opening_report(session, payload)
    return db_obj


@router.put("/opening-reports/{report_id}", response_model=OpeningReportOut)
async def update_opening_report(
    report_id: int, payload: OpeningReportUpdate, session: AsyncSession = Depends(get_session)
):
    db_obj = await crud.update_opening_report(session, report_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_obj