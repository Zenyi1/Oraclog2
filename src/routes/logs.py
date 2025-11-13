from fastapi import APIRouter, HTTPException
from ..models import LogEntry
from ..storage.storage import (
    get_logs, 
    add_log, 
    add_problematic_log, 
    get_logs_by_timestamp
)
from ..services.queue import log_queue
from datetime import datetime

router = APIRouter()

@router.post("/")
async def ingest_log(log: LogEntry):
    try:
        log_dict = log.dict()
        # Add timestamp if not present
        if 'timestamp' not in log_dict:
            log_dict['timestamp'] = datetime.now().isoformat()
        
        # Store in general storage
        add_log(log_dict)
        
        # Queue for rule processing
        await log_queue.put(log_dict)
        return {"message": "Log stored and queued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting log: {e}")

@router.get("/")
async def get_logs_endpoint(limit: int = 10, offset: int = 0, level: str = None):
    try:
        logs, total = get_logs(limit, offset, level)
        return {"logs": logs, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving logs: {e}")

@router.get("/timestamp/{timestamp}")
async def get_logs_by_timestamp_endpoint(timestamp: str):
    try:
        logs = get_logs_by_timestamp(timestamp)
        return {"logs": logs, "total": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving logs by timestamp: {e}")