from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.detection import Detection
from app.models.lost_item import LostItem
from app.models.match import Match
from app.schemas.match import MatchCreate


class MatchNotFoundError(Exception):
    pass


class LostItemNotFoundError(Exception):
    pass


class DetectionNotFoundError(Exception):
    pass


def create_match(db: Session, data: MatchCreate) -> Match:
    # Verify the lost item exists.
    lost_item = db.scalar(
        select(LostItem).where(LostItem.id == data.lost_item_id)
    )

    if lost_item is None:
        raise LostItemNotFoundError(
            f"Lost item with id {data.lost_item_id} was not found."
        )

    # Verify the detection exists.
    detection = db.scalar(
        select(Detection).where(Detection.id == data.detection_id)
    )

    if detection is None:
        raise DetectionNotFoundError(
            f"Detection with id {data.detection_id} was not found."
        )

    match = Match(
        lost_item_id=data.lost_item_id,
        detection_id=data.detection_id,
        match_score=data.match_score,
        decision=data.decision,
        reason=data.reason,
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match


def get_matches(db: Session) -> list[Match]:
    statement = select(Match).order_by(Match.created_at.desc())

    return list(db.scalars(statement).all())


def get_match(db: Session, match_id: int) -> Match | None:
    statement = select(Match).where(Match.id == match_id)

    return db.scalar(statement)