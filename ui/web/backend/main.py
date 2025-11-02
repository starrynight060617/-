"""
FastAPI 后端主程序
"""

from fastapi import FastAPI

app = FastAPI(title="抽象梗日历")

@app.get("/")
async def root():
    return {"message": "抽象梗日历 API"}

@app.get("/events/")
async def get_events():
    return {"events": []}

@app.get("/events/sample")
async def get_sample_events():
    events = load_sample_data()
    return {"events": events}
