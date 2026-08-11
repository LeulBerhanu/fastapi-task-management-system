from typing import Type, TypeVar, Generic
from uuid import UUID
from sqlmodel import SQLModel, Session, select

ModelT = TypeVar('ModelT', bound=SQLModel)

class BaseRepository(Generic[ModelT]):
    def __init__(self, session: Session, model: Type[ModelT]):
        self.session = session
        self.model = model

    def list(self) -> list[ModelT]:
        return self.session.exec(select(self.model)).all()

    def get(self, id: UUID) -> ModelT | None:
        return self.session.exec(
            select(self.model).where(self.model.id == id)
        ).one_or_none()
    
    def create(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: UUID) -> bool:
        obj = self.get(id)
        if obj is None:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
    