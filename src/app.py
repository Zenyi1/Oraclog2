from fastapi import FastAPI
import uvicorn
from .routes.logs import router as logs_router
from .routes.analysis import router as analysis_router

app = FastAPI()

# Include routers with prefixes for organization
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(analysis_router, prefix="/analyze", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "LogOracle API caller"}

port = 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)