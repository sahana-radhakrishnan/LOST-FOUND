from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.detection import DetectionCreate, DetectionResponse
from app.services.detection_service import (
    create_detection,
    get_detection,
    get_detections,
)

router = APIRouter(
    prefix="/detections",
    tags=["Detections"],
)


@router.post(
    "",
    response_model=DetectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_detection_endpoint(
    data: DetectionCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_detection(db, data)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create detection.",
        )


@router.get(
    "",
    response_model=list[DetectionResponse],
)
def list_detections(
    db: Session = Depends(get_db),
):
    try:
        return get_detections(db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve detections.",
        )


@router.get(
    "/{detection_id}",
    response_model=DetectionResponse,
)
def get_detection_by_id(
    detection_id: int,
    db: Session = Depends(get_db),
):
    detection = get_detection(db, detection_id)

    if detection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Detection with id {detection_id} was not found.",
        )

    return detection