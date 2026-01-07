from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.db.models.message import Message
from app.db.models.conversation import Conversation
from app.schemas.message import CreateMessage, UpdateMessage
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDMessage:
    @staticmethod
    async def get_one(db, message_id: int):
        q = (
            select(Message)
            .options(selectinload(Message.sender))
            .where(Message.id == message_id)
        )
        res = await db.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def get_many(db, conversation_id: int, skip: int = 0, limit: int = 50):
        q = (
            select(Message)
            .options(selectinload(Message.sender))
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        res = await db.execute(q)
        return res.scalars().all()

    @staticmethod
    async def create(db, data: CreateMessage, sender_id: int):
        # Check if user is member of conversation
        conv_q = select(Conversation).where(Conversation.id == data.conversation_id)
        conv_res = await db.execute(conv_q)
        conversation = conv_res.scalar_one_or_none()
        if not conversation:
            raise ValueError("Conversation not found")

        # Check membership - assuming members relationship
        is_member = any(member.id == sender_id for member in conversation.members)
        if not is_member:
            raise ValueError("User is not a member of this conversation")

        message = Message(
            conversation_id=data.conversation_id,
            sender_id=sender_id,
            content=data.content,
            type=data.type,
            file=data.file,
        )

        db.add(message)
        await db.flush()  # Get message.id

        # Update conversation's last_message_id
        conversation.last_message_id = message.id
        db.add(conversation)

        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def update(db, message: Message, data: UpdateMessage, user_id: int):
        # Only sender can update
        if message.sender_id != user_id:
            raise ValueError("Only sender can update message")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(message, field):
                setattr(message, field, value)

        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def delete(db, message: Message, user_id: int):
        # Only sender can delete
        if message.sender_id != user_id:
            raise ValueError("Only sender can delete message")

        await db.delete(message)
        await db.commit()


crud_message = CRUDMessage()
