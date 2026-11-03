from fastapi import FastAPI
from database.connection import initialize_database
from routes.users import user_router
from routes.events import event_router
import uvicorn

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
async def on_startup():
    await initialize_database()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)