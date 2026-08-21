from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.lost_item import LostItemCreate, LostItemResponse
from app.services.lost_item_service import (
    create_lost_item,
    get_lost_item,
    get_lost_items,
)

router = APIRouter(
    prefix="/lost-items",
    tags=["Lost Items"],
)


@router.post(
    "",
    response_model=LostItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lost_item_endpoint(
    data: LostItemCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_lost_item(db, data)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create lost item.",
        )


@router.get(
    "",
    response_model=list[LostItemResponse],
)
def list_lost_items(
    db: Session = Depends(get_db),
):
    try:
        return get_lost_items(db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve lost items.",
        )


@router.get(
    "/{item_id}",
    response_model=LostItemResponse,
)
def get_lost_item_by_id(
    item_id: int,
    db: Session = Depends(get_db),
):
    lost_item = get_lost_item(db, item_id)

    if lost_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lost item with id {item_id} was not found.",
        )

    return lost_item