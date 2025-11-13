from fastapi import APIRouter, HTTPException
from ..models import AnalysisRequest
from ..services.service import ai_response
from ..storage.storage import all_logs_storage, add_insight, get_insights

router = APIRouter()

@router.post("/")
async def analyze_log(request: AnalysisRequest):
    try:
        if request.log_id >= len(all_logs_storage) or request.log_id < 0:
            raise HTTPException(status_code=404, detail="Log not found")
        
        log = all_logs_storage[request.log_id]
        prompt = f"{request.prompt_override or 'Analyze this log for incidents'}: {log['message']}"
        analysis = ai_response(prompt)
        add_insight(request.log_id, analysis)
        return {"log_id": request.log_id, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing log: {e}")

@router.get("/insights")
async def get_insights_endpoint(limit: int = 10, offset: int = 0):
    try:
        insights, total = get_insights(limit, offset)
        return {"insights": insights, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving insights: {e}")