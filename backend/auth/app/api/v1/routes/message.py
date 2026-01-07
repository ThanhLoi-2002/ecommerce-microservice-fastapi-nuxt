from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, get_current_user
from app.db.models.user import User
from app.schemas.message import CreateMessage, UpdateMessage, MessageResponse
from app.crud.crud_message import crud_message
from app.socketio.server import sio

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=MessageResponse)
@response_message("Message sent")
async def create_message(
    data: CreateMessage,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    try:
        message = await crud_message.create(db, data, current_user.id)

        # Emit to conversation room
        await sio.emit(
            "new_message",
            {"message": MessageResponse.from_orm(message).model_dump()},
            room=f"conversation_{data.conversation_id}",
        )

        return message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    # Check if user is member (assuming crud_message handles this, but let's verify)
    from app.crud.crud_conversation import crud_conversation

    conv = await crud_conversation.get_one(db, conversation_id, current_user.id)
    if not conv:
        raise HTTPException(status_code=403, detail="Not a member of this conversation")

    messages = await crud_message.get_many(db, conversation_id, skip, limit)
    return messages


@router.put("/{message_id}", response_model=MessageResponse)
@response_message("Message updated")
async def update_message(
    message_id: int,
    data: UpdateMessage,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    message = await crud_message.get_one(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    try:
        updated = await crud_message.update(db, message, data, current_user.id)

        # Emit update to conversation room
        await sio.emit(
            "message_updated",
            {"message": MessageResponse.from_orm(updated).model_dump()},
            room=f"conversation_{message.conversation_id}",
        )

        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{message_id}")
@response_message("Message deleted")
async def delete_message(
    message_id: int,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    message = await crud_message.get_one(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    try:
        await crud_message.delete(db, message, current_user.id)

        # Emit delete to conversation room
        await sio.emit(
            "message_deleted",
            {"message_id": message_id, "conversation_id": message.conversation_id},
            room=f"conversation_{message.conversation_id}",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
