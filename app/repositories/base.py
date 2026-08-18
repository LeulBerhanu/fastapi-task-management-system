from typing import Type, TypeVar, Generic
from uuid import UUID
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelT = TypeVar('ModelT', bound=SQLModel)

class BaseRepository(Generic[ModelT]):
    def __init__(self, async_session: AsyncSession, model: Type[ModelT]):
        self.async_session = async_session
        self.model = model

    async def list(self) -> list[ModelT]:
        response = await self.async_session.exec(select(self.model))
        return response.all()

    async def get_by_id(self, id: UUID) -> ModelT | None:
        response = await self.async_session.exec(
            select(self.model).where(self.model.id == id)
        )
        return response.one_or_none()
    
    async def create(self, obj: ModelT) -> ModelT:
        self.async_session.add(obj)
        await self.async_session.flush()
        await self.async_session.refresh(obj)
        return obj

    async def delete(self, id: UUID) -> bool:
        obj = await self.get_by_id(id)
        if obj is None:
            return False
        await self.async_session.delete(obj)
        await self.async_session.flush()
        return True
    