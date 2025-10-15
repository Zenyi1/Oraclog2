from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str

class LogEntry(BaseModel):
    source: str
    level: str
    message: str
    timestamp: str

class AnalysisRequest(BaseModel):
    log_id: int
    prompt_override: str = None