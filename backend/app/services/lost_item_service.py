from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lost_item import LostItem
from app.schemas.lost_item import LostItemCreate


def create_lost_item(db: Session, data: LostItemCreate) -> LostItem:
    lost_item = LostItem(
        item_name=data.item_name,
        description=data.description,
        location=data.location,
        lost_time=data.lost_time,
        contact=data.contact,
    )

    db.add(lost_item)
    db.commit()
    db.refresh(lost_item)

    return lost_item


def get_lost_items(db: Session) -> list[LostItem]:
    statement = select(LostItem).order_by(LostItem.created_at.desc())

    return list(db.scalars(statement).all())


def get_lost_item(db: Session, item_id: int) -> LostItem | None:
    statement = select(LostItem).where(LostItem.id == item_id)

    return db.scalar(statement)