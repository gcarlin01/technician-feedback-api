from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback
from app.schemas import FeedbackCreate, FeedbackRead, FeedbackUpdate


router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])


@router.get("", response_model=List[FeedbackRead])
def list_feedback(db: Session = Depends(get_db)) -> List[Feedback]:
    statement = select(Feedback).order_by(Feedback.created_at.desc(), Feedback.id.desc())
    return list(db.scalars(statement).all())


@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)) -> Feedback:
    feedback = db.get(Feedback, feedback_id)
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback


@router.post("", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)) -> Feedback:
    feedback = Feedback(**payload.model_dump())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.put("/{feedback_id}", response_model=FeedbackRead)
def update_feedback(
    feedback_id: int,
    payload: FeedbackUpdate,
    db: Session = Depends(get_db),
) -> Feedback:
    feedback = db.get(Feedback, feedback_id)
    if feedback is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    for field, value in payload.model_dump().items():
        setattr(feedback, field, value)
    db.commit()
    db.refresh(feedback)
    return feedback
