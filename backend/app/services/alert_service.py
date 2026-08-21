from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.match import Match
from app.schemas.alert import AlertCreate


class MatchNotFoundError(Exception):
    pass


def create_alert(db: Session, data: AlertCreate) -> Alert:
    # Verify that the referenced match exists.
    match = db.scalar(
        select(Match).where(Match.id == data.match_id)
    )

    if match is None:
        raise MatchNotFoundError(
            f"Match with id {data.match_id} was not found."
        )

    alert = Alert(
        match_id=data.match_id,
        alert_type=data.alert_type,
        message=data.message,
        status=data.status,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alerts(db: Session) -> list[Alert]:
    statement = select(Alert).order_by(Alert.created_at.desc())

    return list(db.scalars(statement).all())