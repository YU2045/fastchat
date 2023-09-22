from fastapi import APIRouter

router = APIRouter()


@router.put('/messages/{message_id}/like', response_model=None)
async def increment_like():
    pass
