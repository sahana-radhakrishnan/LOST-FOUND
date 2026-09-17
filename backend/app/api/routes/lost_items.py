import sys
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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


def run_investigation(lost_item_id: int):
    """
    Run the investigation agent automatically after a lost item
    has been successfully created.
    """

    try:
        from agent.agent import LostFoundAgent

        agent = LostFoundAgent()
        result = agent.investigate(lost_item_id)

        print(
            f"[AGENT] Investigation completed for "
            f"lost item {lost_item_id}: "
            f"{result.get('status')}"
        )

    except Exception as exc:
        print(
            f"[AGENT] Investigation failed for "
            f"lost item {lost_item_id}: {exc}"
        )


@router.post(
    "",
    response_model=LostItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lost_item_endpoint(
    data: LostItemCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    User submits a lost-item report.

    The backend stores it and automatically starts
    the investigation agent in the background.
    """

    try:
        lost_item = create_lost_item(db, data)

        background_tasks.add_task(
            run_investigation,
            lost_item.id,
        )

        return lost_item

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