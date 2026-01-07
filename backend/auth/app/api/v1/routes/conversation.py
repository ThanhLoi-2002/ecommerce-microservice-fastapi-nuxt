from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, get_current_user
from app.db.models.user import User
from app.schemas.conversation import (
    CreateConversation,
    UpdateConversation,
    ConversationResponse,
)
from app.crud.crud_conversation import crud_conversation
from app.socketio.server import sio

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=ConversationResponse)
@response_message("Conversation created")
async def create_conversation(
    data: CreateConversation,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    try:
        conversation = await crud_conversation.create(db, data, current_user.id)

        # Emit to all members
        for member in conversation.members:
            await sio.emit(
                "conversation_created",
                {
                    "conversation": ConversationResponse.from_orm(
                        conversation
                    ).model_dump()
                },
                room=f"user_{member.id}",
            )

        return conversation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    conversations = await crud_conversation.get_many(db, current_user.id, skip, limit)
    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    conversation = await crud_conversation.get_one(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.put("/{conversation_id}", response_model=ConversationResponse)
@response_message("Conversation updated")
async def update_conversation(
    conversation_id: int,
    data: UpdateConversation,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    conversation = await crud_conversation.get_one(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if user is owner or admin
    is_admin = any(admin.user_id == current_user.id for admin in conversation.admins)
    if conversation.owner_id != current_user.id and not is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update conversation"
        )

    updated = await crud_conversation.update(db, conversation, data)

    # Emit update to all members
    for member in updated.members:
        await sio.emit(
            "conversation_updated",
            {"conversation": ConversationResponse.from_orm(updated).model_dump()},
            room=f"user_{member.id}",
        )

    return updated


@router.delete("/{conversation_id}")
@response_message("Conversation deleted")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_user),
):
    conversation = await crud_conversation.get_one(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Only owner can delete
    if conversation.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only owner can delete conversation"
        )

    await crud_conversation.delete(db, conversation)

    # Emit delete to all members
    for member in conversation.members:
        await sio.emit(
            "conversation_deleted",
            {"conversation_id": conversation_id},
            room=f"user_{member.id}",
        )
