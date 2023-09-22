from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.message as message_model
import api.schemas.message as message_schema


async def get_messages(db: AsyncSession) -> list[tuple[int, str, str, int]]:
    result: Result = await (
        db.execute(
            select(
                message_model.Message.id,
                message_model.Message.user,
                message_model.Message.text,
                message_model.Message.like,
            )
        )
    )

    return result.all()


async def add_message(
    db: AsyncSession,
    message_add: message_schema.MessageAdd
) -> message_model.Message:
    message = message_model.Message(**message_add.model_dump())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_message(db: AsyncSession, message_id: int) -> message_model.Message | None:
    result: Result = await db.execute(
        select(message_model.Message).filter(message_model.Message.id == message_id)
    )
    message: tuple[message_model.Message] | None = result.first()
    return message[0] if message is not None else None


async def increment_like(db: AsyncSession, message_id: int):
    result: Result = await db.execute(
        select(message_model.Message).filter(message_model.Message.id == message_id)
    )
    message: tuple[message_model.Message] | None = result.first()
    if message is None:
        return

    original = message[0]
    original.like += 1
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def update_message(
    db: AsyncSession, message_add: message_schema.MessageAdd, original: message_model.Message
) -> message_model.Message:
    original.text = message_add.text
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_message(db: AsyncSession, original: message_model.Message) -> None:
    await db.delete(original)
    await db.commit()
