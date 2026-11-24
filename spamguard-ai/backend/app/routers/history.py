"""
Scan history router supporting search, filtering, and session reset.
"""
from fastapi import APIRouter, Query
from typing import Optional
from app.models import HistoryResponse
from app.services.history_store import HistoryStore

router = APIRouter(prefix="/history", tags=["Scan History"])

@router.get("", response_model=HistoryResponse)
def get_history(
    filter: Optional[str] = Query(None, description="Filter by decision: ALL, SPAM, HAM, SUSPICIOUS"),
    label: Optional[str] = Query(None, description="Alias for filter"),
    threat_level: Optional[str] = Query(None, description="Filter by threat level: LOW, MEDIUM, HIGH, CRITICAL"),
    search: Optional[str] = Query(None, description="Search keyword in message"),
    limit: Optional[int] = Query(None, ge=1, le=200),
    page_size: Optional[int] = Query(None, ge=1, le=200),
    offset: Optional[int] = Query(None, ge=0),
    page: Optional[int] = Query(None, ge=1)
):
    """Returns paginated scan records with optional decision filtering and text search."""
    store = HistoryStore.get_instance()
    
    # Resolve decision filter
    raw_filter = filter or label or "ALL"
    decision_filter = None if raw_filter.upper() == "ALL" else raw_filter

    # Resolve pagination
    effective_limit = limit or page_size or 50
    if offset is not None:
        effective_offset = offset
    elif page is not None and page > 0:
        effective_offset = (page - 1) * effective_limit
    else:
        effective_offset = 0

    return store.get_entries(
        decision_filter=decision_filter,
        search_query=search,
        limit=effective_limit,
        offset=effective_offset
    )

@router.delete("")
def clear_history():
    """Clears in-memory session history."""
    store = HistoryStore.get_instance()
    store.clear()
    return {"status": "success", "message": "Session scan history successfully cleared."}
