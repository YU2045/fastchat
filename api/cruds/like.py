from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.message as message_model


async def get_like(db: AsyncSession, message_id: int) -> message_model.Like | None:
    result: Result = await db.execute(
        select(message_model.Like).filter(message_model.Like.id == message_id)
    )
    like: tuple[message_model.Like] | None = result.first()
    return like[0] if like is not None else None


async def create_like(db: AsyncSession, message_id: int) -> message_model.Like:
    like = message_model.Like(id=message_id)
    db.add(like)
    await db.commit()
    await db.refresh(like)
    return like


async def delete_like(db: AsyncSession, original: message_model.Like) -> None:
    await db.delete(original)
    await db.commit()
