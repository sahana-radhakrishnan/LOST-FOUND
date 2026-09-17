from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.alert import AlertCreate, AlertResponse
from app.services.alert_service import (
    MatchNotFoundError,
    create_alert,
    get_alerts,
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alert_endpoint(
    data: AlertCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_alert(db, data)

    except MatchNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create alert.",
        )


@router.get(
    "",
    response_model=list[AlertResponse],
)
def list_alerts(
    db: Session = Depends(get_db),
):
    try:
        return get_alerts(db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve alerts.",
        )