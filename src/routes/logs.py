from fastapi import APIRouter, HTTPException
from ..models import LogEntry
from ..storage.storage import get_logs, logs_storage
from ..services.queue import log_queue

router = APIRouter()

@router.post("/")
async def ingest_log(log: LogEntry):
    try:
        await log_queue.put(log.dict())
        return {"message": "queued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting log: {e}")

@router.get("/")
async def get_logs_endpoint(limit: int = 10, offset: int = 0, level: str = None):
    try:
        logs, total = get_logs(limit, offset, level)
        return {"logs": logs, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving logs: {e}")