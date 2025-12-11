from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field


def calc_total_score(
    process_score: Optional[float],
    opening_score: Optional[float],
    midterm_score: Optional[float],
    thesis_score: Optional[float],
    defense_score: Optional[float],
) -> float:
    return (
        (process_score or 0) * 0.2
        + (opening_score or 0) * 0.1
        + (midterm_score or 0) * 0.1
        + (thesis_score or 0) * 0.3
        + (defense_score or 0) * 0.3
    )


def calc_score_level(total: float) -> str:
    if total >= 90:
        return "A"
    if total >= 80:
        return "B"
    if total >= 70:
        return "C"
    if total >= 60:
        return "D"
    return "F"


class ScoreBase(BaseModel):
    student_id: int = Field(...)
    topic_id: int = Field(...)
    process_score: Optional[float] = Field(None, ge=0, le=100)
    opening_score: Optional[float] = Field(None, ge=0, le=100)
    midterm_score: Optional[float] = Field(None, ge=0, le=100)
    thesis_score: Optional[float] = Field(None, ge=0, le=100)
    defense_score: Optional[float] = Field(None, ge=0, le=100)
    is_published: int = Field(0, ge=0, le=1)

    model_config = {"extra": "forbid"}


class ScoreCreate(ScoreBase):
    pass


class ScoreUpdate(BaseModel):
    student_id: Optional[int] = Field(None)
    topic_id: Optional[int] = Field(None)
    process_score: Optional[float] = Field(None, ge=0, le=100)
    opening_score: Optional[float] = Field(None, ge=0, le=100)
    midterm_score: Optional[float] = Field(None, ge=0, le=100)
    thesis_score: Optional[float] = Field(None, ge=0, le=100)
    defense_score: Optional[float] = Field(None, ge=0, le=100)
    is_published: Optional[int] = Field(None, ge=0, le=1)

    model_config = {"extra": "forbid"}


class ScoreOut(ScoreBase):
    id: int
    total_score: Optional[float] = None
    score_level: Optional[str] = None

    model_config = {"from_attributes": True, "extra": "ignore"}

    @computed_field
    @property
    def total(self) -> float:
        return self.total_score or calc_total_score(
            self.process_score,
            self.opening_score,
            self.midterm_score,
            self.thesis_score,
            self.defense_score,
        )


class PaginatedScores(BaseModel):
    items: list[ScoreOut]
    total: int


class BatchStatusRequest(BaseModel):
    ids: list[int] = Field(..., min_length=1)
    is_published: int = Field(..., ge=0, le=1)


class StatsResponse(BaseModel):
    count: int
    avg: float
    max: float
    min: float
    pass_rate: float
    excellent_rate: float


# 课题申报通知（DECLARATION_NOTICE）
class NoticeBase(BaseModel):
    title: str
    type: str = Field(..., description="初次申报/二次补申报")
    majors: list[str] = Field(default_factory=list)
    teacher_scope: str = ""
    requirement: str = ""
    auto_remind: bool = True
    start_time: datetime
    end_time: datetime
    status: str = Field(default="草稿", description="草稿/已发布/已撤回")

    model_config = {"extra": "ignore"}


class NoticeCreate(NoticeBase):
    publisher: str = "教科办"


class NoticeUpdate(NoticeBase):
    publisher: Optional[str] = None


class NoticeOut(NoticeBase):
    id: int
    declare_type: str
    publish_time: Optional[datetime] = None
    is_deleted: int = 0

    model_config = {"from_attributes": True}


# 课题信息（THESIS_TOPIC）
class TopicBase(BaseModel):
    topic_name: str
    teacher_id: int
    topic_type: str
    content: Optional[str] = None
    expected_result: Optional[str] = None
    major_limit: Optional[str] = None
    max_students: int = 1
    audit_status: str = "待审核"
    audit_opinion: Optional[str] = None
    publish_status: int = 0

    model_config = {"extra": "ignore"}


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    topic_name: Optional[str] = None
    teacher_id: Optional[int] = None
    topic_type: Optional[str] = None
    content: Optional[str] = None
    expected_result: Optional[str] = None
    major_limit: Optional[str] = None
    max_students: Optional[int] = None
    audit_status: Optional[str] = None
    audit_opinion: Optional[str] = None
    publish_status: Optional[int] = None

    model_config = {"extra": "ignore"}


class TopicOut(TopicBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# 资料归档（ARCHIVE_DOC）
class ArchiveDocBase(BaseModel):
    student_id: int
    file_name: str
    file_type: str
    file_path: str
    version: str = "v1.0"
    audit_status: str = "待审核"

    model_config = {"extra": "ignore"}


class ArchiveDocCreate(ArchiveDocBase):
    pass


class ArchiveDocUpdate(BaseModel):
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_path: Optional[str] = None
    version: Optional[str] = None
    audit_status: Optional[str] = None

    model_config = {"extra": "ignore"}


class ArchiveDocOut(ArchiveDocBase):
    id: int
    upload_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


# 中期检查（MIDTERM_CHECK）
class MidtermCheckBase(BaseModel):
    student_id: int
    completed_content: Optional[str] = None
    problems: Optional[str] = None
    next_plan: Optional[str] = None
    progress_status: str = "正常"
    teacher_feedback: Optional[str] = None
    check_result: Optional[str] = None

    model_config = {"extra": "ignore"}


class MidtermCheckCreate(MidtermCheckBase):
    pass


class MidtermCheckUpdate(BaseModel):
    completed_content: Optional[str] = None
    problems: Optional[str] = None
    next_plan: Optional[str] = None
    progress_status: Optional[str] = None
    teacher_feedback: Optional[str] = None
    check_result: Optional[str] = None

    model_config = {"extra": "ignore"}


class MidtermCheckOut(MidtermCheckBase):
    id: int
    submit_time: Optional[datetime] = None

    model_config = {"from_attributes": True}


# 开题报告（OPENING_REPORT）
class OpeningReportBase(BaseModel):
    student_id: int
    topic_id: int
    background: Optional[str] = None
    target: Optional[str] = None
    method: Optional[str] = None
    plan: Optional[str] = None
    report_status: str = "待审核"
    teacher_comment: Optional[str] = None

    model_config = {"extra": "ignore"}


class OpeningReportCreate(OpeningReportBase):
    pass


class OpeningReportUpdate(BaseModel):
    background: Optional[str] = None
    target: Optional[str] = None
    method: Optional[str] = None
    plan: Optional[str] = None
    report_status: Optional[str] = None
    teacher_comment: Optional[str] = None

    model_config = {"extra": "ignore"}


class OpeningReportOut(OpeningReportBase):
    id: int
    submit_time: Optional[datetime] = None
    audit_time: Optional[datetime] = None

    model_config = {"from_attributes": True}
