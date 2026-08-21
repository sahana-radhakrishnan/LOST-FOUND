from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.detection import Detection
from app.schemas.detection import DetectionCreate


def create_detection(db: Session, data: DetectionCreate) -> Detection:
    detection = Detection(
        camera_id=data.camera_id,
        location=data.location,
        object=data.object,
        confidence=data.confidence,
        timestamp=data.timestamp,
        image_path=data.image_path,
    )

    db.add(detection)
    db.commit()
    db.refresh(detection)

    return detection


def get_detections(db: Session) -> list[Detection]:
    statement = select(Detection).order_by(Detection.created_at.desc())

    return list(db.scalars(statement).all())


def get_detection(db: Session, detection_id: int) -> Detection | None:
    statement = select(Detection).where(Detection.id == detection_id)

    return db.scalar(statement)