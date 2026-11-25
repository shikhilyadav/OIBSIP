"""
Dataset Explorer Router (GET /api/dataset/summary, GET /api/dataset/records)
Serves authentic UCI SMS Spam Collection dataset records without modification.
"""
from pathlib import Path
from typing import Optional, List
import pandas as pd
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel

from ..config import TASK4_DATASET

router = APIRouter(prefix="/dataset", tags=["Dataset Explorer"])

_df_cache = None

def get_dataset_df() -> pd.DataFrame:
    global _df_cache
    if _df_cache is None:
        if not TASK4_DATASET.exists():
            raise HTTPException(status_code=404, detail="Original Task 4 dataset spam.csv not found.")
        df = pd.read_csv(TASK4_DATASET, encoding="latin-1")
        # Keep canonical columns: label and message
        clean_df = pd.DataFrame({
            "id": range(1, len(df) + 1),
            "label": df["v1"].astype(str).str.lower().str.strip(),
            "message": df["v2"].astype(str),
        })
        clean_df["char_length"] = clean_df["message"].str.len()
        clean_df["word_count"] = clean_df["message"].apply(lambda m: len(m.split()))
        _df_cache = clean_df
    return _df_cache


class DatasetSummaryResponse(BaseModel):
    total_messages: int
    ham_count: int
    spam_count: int
    spam_percentage: float
    ham_percentage: float
    avg_char_length: float
    avg_word_count: float
    max_char_length: int
    min_char_length: int


class MessageRecord(BaseModel):
    id: int
    label: str
    message: str
    char_length: int
    word_count: int


class DatasetRecordsResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    records: List[MessageRecord]


@router.get("/summary", response_model=DatasetSummaryResponse)
def get_dataset_summary():
    """Returns descriptive statistical moments of the authentic 5,572-message dataset."""
    df = get_dataset_df()
    total = len(df)
    ham_count = int((df["label"] == "ham").sum())
    spam_count = int((df["label"] == "spam").sum())

    return {
        "total_messages": total,
        "ham_count": ham_count,
        "spam_count": spam_count,
        "spam_percentage": round((spam_count / total) * 100, 2),
        "ham_percentage": round((ham_count / total) * 100, 2),
        "avg_char_length": round(float(df["char_length"].mean()), 1),
        "avg_word_count": round(float(df["word_count"].mean()), 1),
        "max_char_length": int(df["char_length"].max()),
        "min_char_length": int(df["char_length"].min()),
    }


@router.get("/records", response_model=DatasetRecordsResponse)
def get_dataset_records(
    label: Optional[str] = Query(None, description="Filter by label: ham, spam, or all"),
    search: Optional[str] = Query(None, description="Search keyword in message text"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Records per page")
):
    """Returns paginated, searchable, filterable dataset records."""
    df = get_dataset_df()
    filtered = df.copy()

    if label and label.lower() != "all":
        filtered = filtered[filtered["label"] == label.lower()]

    if search:
        q = search.lower().strip()
        filtered = filtered[filtered["message"].str.lower().str.contains(q, na=False)]

    total = len(filtered)
    total_pages = max(1, (total + page_size - 1) // page_size)

    start = (page - 1) * page_size
    end = start + page_size
    records = filtered.iloc[start:end].to_dict(orient="records")

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "records": records
    }
