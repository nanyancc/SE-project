from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class GraduationScore(Base):
    __tablename__ = "GRADUATION_SCORE"

    id: Mapped[int] = mapped_column("SCORE_ID", Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        "STUDENT_ID", Integer, nullable=False, unique=True, index=True
    )
    topic_id: Mapped[int] = mapped_column("TOPIC_ID", Integer, nullable=False, index=True)
    process_score: Mapped[float | None] = mapped_column("PROCESS_SCORE", Numeric(5, 2))
    opening_score: Mapped[float | None] = mapped_column("OPENING_SCORE", Numeric(5, 2))
    midterm_score: Mapped[float | None] = mapped_column("MIDTERM_SCORE", Numeric(5, 2))
    thesis_score: Mapped[float | None] = mapped_column("THESIS_SCORE", Numeric(5, 2))
    defense_score: Mapped[float | None] = mapped_column("DEFENSE_SCORE", Numeric(5, 2))
    total_score: Mapped[float | None] = mapped_column("TOTAL_SCORE", Numeric(5, 2))
    score_level: Mapped[str | None] = mapped_column("SCORE_LEVEL", String(2))
    is_published: Mapped[int] = mapped_column(
        "IS_PUBLISHED", Integer, nullable=False, default=0, server_default="0"
    )


class DeclarationNotice(Base):
    __tablename__ = "DECLARATION_NOTICE"

    id: Mapped[int] = mapped_column("NOTICE_ID", Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column("NOTICE_TITLE", String(200), nullable=False)
    content: Mapped[str | None] = mapped_column("NOTICE_CONTENT", Text, nullable=True)
    declare_type: Mapped[str] = mapped_column(
        "DECLARE_TYPE", String(1), nullable=False, default="1", server_default="1"
    )
    start_time: Mapped[datetime] = mapped_column("START_TIME", DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column("END_TIME", DateTime, nullable=False)
    publisher: Mapped[str] = mapped_column("PUBLISHER", String(50), nullable=False)
    publish_time: Mapped[datetime | None] = mapped_column(
        "PUBLISH_TIME", DateTime, nullable=True, server_default=func.now()
    )
    is_deleted: Mapped[int] = mapped_column(
        "IS_DELETED", Integer, nullable=False, default=0, server_default="0"
    )


class ThesisTopic(Base):
    __tablename__ = "THESIS_TOPIC"

    id: Mapped[int] = mapped_column("TOPIC_ID", Integer, primary_key=True, index=True)
    topic_name: Mapped[str] = mapped_column("TOPIC_NAME", String(200), nullable=False)
    teacher_id: Mapped[int] = mapped_column("TEACHER_ID", Integer, nullable=False)
    topic_type: Mapped[str] = mapped_column("TOPIC_TYPE", String(20), nullable=False)
    content: Mapped[str | None] = mapped_column("CONTENT", Text, nullable=True)
    expected_result: Mapped[str | None] = mapped_column(
        "EXPECTED_RESULT", Text, nullable=True
    )
    major_limit: Mapped[str | None] = mapped_column(
        "MAJOR_LIMIT", String(100), nullable=True
    )
    max_students: Mapped[int] = mapped_column(
        "MAX_STUDENTS", Integer, nullable=False, default=1, server_default="1"
    )
    audit_status: Mapped[str] = mapped_column(
        "AUDIT_STATUS", String(20), nullable=False, default="待审核", server_default="待审核"
    )
    audit_opinion: Mapped[str | None] = mapped_column(
        "AUDIT_OPINION", String(500), nullable=True
    )
    publish_status: Mapped[int] = mapped_column(
        "PUBLISH_STATUS", Integer, nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class TopicSelection(Base):
    __tablename__ = "TOPIC_SELECTION"

    id: Mapped[int] = mapped_column("SELECT_ID", Integer, primary_key=True, index=True)
    topic_id: Mapped[int] = mapped_column("TOPIC_ID", Integer, nullable=False, index=True)
    student_id: Mapped[int] = mapped_column(
        "STUDENT_ID", Integer, nullable=False, index=True
    )
    volunteer_order: Mapped[int] = mapped_column(
        "VOLUNTEER_ORDER", Integer, nullable=False, default=1, server_default="1"
    )
    select_status: Mapped[str] = mapped_column(
        "SELECT_STATUS", String(20), nullable=False, default="待确认", server_default="待确认"
    )
    select_time: Mapped[datetime | None] = mapped_column(
        "SELECT_TIME", DateTime, nullable=True, server_default=func.now()
    )


class ArchiveDoc(Base):
    __tablename__ = "ARCHIVE_DOC"

    id: Mapped[int] = mapped_column("DOC_ID", Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column("STUDENT_ID", Integer, nullable=False, index=True)
    file_name: Mapped[str] = mapped_column("FILE_NAME", String(255), nullable=False)
    file_type: Mapped[str] = mapped_column("FILE_TYPE", String(50), nullable=False)
    file_path: Mapped[str] = mapped_column("FILE_PATH", String(500), nullable=False)
    version: Mapped[str] = mapped_column(
        "VERSION", String(10), nullable=False, default="v1.0", server_default="v1.0"
    )
    upload_time: Mapped[datetime | None] = mapped_column(
        "UPLOAD_TIME", DateTime, nullable=True, server_default=func.now()
    )
    audit_status: Mapped[str] = mapped_column(
        "AUDIT_STATUS", String(20), nullable=False, default="待审核", server_default="待审核"
    )


class MidtermCheck(Base):
    __tablename__ = "MIDTERM_CHECK"

    id: Mapped[int] = mapped_column("CHECK_ID", Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        "STUDENT_ID", Integer, nullable=False, unique=True, index=True
    )
    completed_content: Mapped[str | None] = mapped_column(
        "COMPLETED_CONTENT", Text, nullable=True
    )
    problems: Mapped[str | None] = mapped_column("PROBLEMS", Text, nullable=True)
    next_plan: Mapped[str | None] = mapped_column("NEXT_PLAN", Text, nullable=True)
    progress_status: Mapped[str] = mapped_column(
        "PROGRESS_STATUS", String(20), nullable=False, default="正常", server_default="正常"
    )
    teacher_feedback: Mapped[str | None] = mapped_column(
        "TEACHER_FEEDBACK", String(500), nullable=True
    )
    check_result: Mapped[str | None] = mapped_column(
        "CHECK_RESULT", String(20), nullable=True
    )
    submit_time: Mapped[datetime | None] = mapped_column(
        "SUBMIT_TIME", DateTime, nullable=True, server_default=func.now()
    )


class OpeningReport(Base):
    __tablename__ = "OPENING_REPORT"

    id: Mapped[int] = mapped_column("REPORT_ID", Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        "STUDENT_ID", Integer, nullable=False, unique=True, index=True
    )
    topic_id: Mapped[int] = mapped_column("TOPIC_ID", Integer, nullable=False, index=True)
    background: Mapped[str | None] = mapped_column("BACKGROUND", Text, nullable=True)
    target: Mapped[str | None] = mapped_column("TARGET", String(1000), nullable=True)
    method: Mapped[str | None] = mapped_column("METHOD", Text, nullable=True)
    plan: Mapped[str | None] = mapped_column("PLAN", Text, nullable=True)
    submit_time: Mapped[datetime | None] = mapped_column(
        "SUBMIT_TIME", DateTime, nullable=True, server_default=func.now()
    )
    report_status: Mapped[str] = mapped_column(
        "REPORT_STATUS", String(20), nullable=False, default="待审核", server_default="待审核"
    )
    teacher_comment: Mapped[str | None] = mapped_column(
        "TEACHER_COMMENT", String(500), nullable=True
    )
    audit_time: Mapped[datetime | None] = mapped_column("AUDIT_TIME", DateTime, nullable=True)
