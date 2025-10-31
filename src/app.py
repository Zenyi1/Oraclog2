from fastapi import FastAPI
import uvicorn
import asyncio
from .routes.logs import router as logs_router
from .routes.analysis import router as analysis_router
from .routes.rules import router as rules_router
from .services.queue import consume_logs

app = FastAPI()

# Include routers with prefixes for organization
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(analysis_router, prefix="/analyze", tags=["Analysis"])
app.include_router(rules_router, prefix="/rules", tags=["Rules"])

@app.on_event("startup")
async def start_consumer():
    print("Starting log consumer...")
    asyncio.create_task(consume_logs()) 

@app.get("/")
async def root():
    return {"message": "LogOracle API caller"}

port = 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)