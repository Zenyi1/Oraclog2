from pydantic import BaseModelm, Optional

class PromptRequest(BaseModel):
    prompt: str

class LogEntry(BaseModel):
    source: str
    level: str
    message: str
    timestamp: str

class batchLogRequest(BaseModel):
    logs: list[LogEntry]

class AnalysisRequest(BaseModel):
    log_id: int
    prompt_override: str = None

class Rule(BaseModel):
    id: int
    keyword: str
    level: Optional[str] = None
