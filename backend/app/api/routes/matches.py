from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.match import MatchCreate, MatchResponse
from app.services.match_service import (
    DetectionNotFoundError,
    LostItemNotFoundError,
    create_match,
    get_match,
    get_matches,
)

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)


@router.post(
    "",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_match_endpoint(
    data: MatchCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_match(db, data)

    except LostItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except DetectionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create match.",
        )


@router.get(
    "",
    response_model=list[MatchResponse],
)
def list_matches(
    db: Session = Depends(get_db),
):
    try:
        return get_matches(db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve matches.",
        )


@router.get(
    "/{match_id}",
    response_model=MatchResponse,
)
def get_match_by_id(
    match_id: int,
    db: Session = Depends(get_db),
):
    match = get_match(db, match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} was not found.",
        )

    return match