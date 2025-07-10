from fastapi import FastAPI
from routes import router
from auth import key_manager
import asyncio

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def start_key_rotation():
    async def rotate():
        while True:
            await asyncio.sleep(60)  # check every 60 seconds
            if key_manager.should_rotate():
                key_manager.rotate_key()
    asyncio.create_task(rotate())
