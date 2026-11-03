from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from models.events import Event
from models.users import User

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    class Config:
        env_file = ".env"

async def initialize_database():
    settings = Settings()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.get_default_database(), document_models=[Event, User])

class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: str) -> Any:
        doc = await self.model.get(id)
        return doc if doc else False

    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()

    async def update(self, id: str, body: BaseModel) -> Any:
        doc = await self.get(id)
        if not doc: return False
        des_body = {k: v for k, v in body.model_dump().items() if v is not None}
        update_query = {"$set": des_body}
        await doc.update(update_query)
        return doc

    async def delete(self, id: str) -> bool:
        doc = await self.get(id)
        if not doc: return False
        await doc.delete()
        return True