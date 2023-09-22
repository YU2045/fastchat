from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.message as message_crud
from api.db import get_db
import api.schemas.message as message_schema

router = APIRouter()


@router.get('/messages', response_model=list[message_schema.Message])
async def list_messages(db: AsyncSession = Depends(get_db)):
    return await message_crud.get_messages(db)


@router.post('/messages', response_model=message_schema.MessageAddResponse)
async def add_message(
    message_body: message_schema.MessageAdd,
    db: AsyncSession = Depends(get_db)
):
    return await message_crud.add_message(db, message_body)


@router.put('/messages/{message_id}', response_model=None)
async def update_like(
    message_id: int,
    db: AsyncSession = Depends(get_db)
):
    message = await message_crud.get_message(db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=404, detail='Message not found')

    return await message_crud.increment_like(db, message_id=message_id)


@router.delete('/messages/{message_id}', response_model=None)
async def delete_message(message_id: int, db: AsyncSession = Depends(get_db)):
    message = await message_crud.get_message(db, message_id=message_id)
    if message is None:
        HTTPException(status_code=404, detail='Message not found')

    return await message_crud.delete_message(db, original=message)
