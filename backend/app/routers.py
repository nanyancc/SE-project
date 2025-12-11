from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .database import get_session
from .schemas import (
    BatchStatusRequest,
    PaginatedScores,
    ScoreCreate,
    ScoreOut,
    ScoreUpdate,
    StatsResponse,
)

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/", response_model=PaginatedScores)
async def list_scores(
    student_id: int | None = Query(None, alias="studentId"),
    topic_id: int | None = Query(None, alias="topicId"),
    score_range: str | None = Query(None, alias="range"),
    level: str | None = Query(None),
    published: int | None = Query(None, alias="published"),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    items, total = await crud.list_scores(
        session,
        student_id,
        topic_id,
        score_range,
        level,
        published,
        limit,
        offset,
    )
    return {"items": items, "total": total}


@router.get("/stats", response_model=StatsResponse)
async def score_stats(
    student_id: int | None = Query(None, alias="studentId"),
    topic_id: int | None = Query(None, alias="topicId"),
    score_range: str | None = Query(None, alias="range"),
    level: str | None = Query(None),
    published: int | None = Query(None, alias="published"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.get_stats(
        session,
        student_id,
        topic_id,
        score_range,
        level,
        published,
    )


@router.post("/", response_model=ScoreOut, status_code=201)
async def create_score(
    payload: ScoreCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_score(session, payload)


@router.put("/{score_id}", response_model=ScoreOut)
async def update_score(
    score_id: int,
    payload: ScoreUpdate,
    session: AsyncSession = Depends(get_session),
):
    db_obj = await crud.update_score(session, score_id, payload)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Score not found")
    return db_obj


@router.post("/batch/status")
async def update_status(
    body: BatchStatusRequest, session: AsyncSession = Depends(get_session)
):
    updated = await crud.batch_update_status(
        session, body.ids, body.is_published
    )
    return {"updated": updated}
