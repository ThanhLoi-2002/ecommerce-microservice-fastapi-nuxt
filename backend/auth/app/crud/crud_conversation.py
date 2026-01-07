from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.conversation import (
    Conversation,
    conversation_members,
    ConversationAdmins,
)
from app.db.models.message import Message
from app.db.models.user import User
from app.schemas.conversation import CreateConversation, UpdateConversation
from typing import Optional


class CRUDConversation:
    @staticmethod
    async def get_one(db, conversation_id: int, user_id: Optional[int] = None):
        q = (
            select(Conversation)
            .options(
                selectinload(Conversation.members),
                selectinload(Conversation.owner),
                selectinload(Conversation.admins),
                selectinload(Conversation.last_message),
            )
            .where(Conversation.id == conversation_id)
        )

        if user_id:
            # Ensure user is a member
            q = q.where(Conversation.members.any(User.id == user_id))

        res = await db.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def get_many(db, user_id: int, skip: int = 0, limit: int = 100):
        q = (
            select(Conversation)
            .options(
                selectinload(Conversation.members),
                selectinload(Conversation.owner),
                selectinload(Conversation.admins),
                selectinload(Conversation.last_message),
            )
            .where(Conversation.members.any(User.id == user_id))
            .offset(skip)
            .limit(limit)
        )

        res = await db.execute(q)
        return res.scalars().all()

    @staticmethod
    async def create(db, data: CreateConversation, creator_id: int):
        # Validate members
        member_users = await db.execute(
            select(User).where(User.id.in_(data.member_ids))
        )
        members = member_users.scalars().all()
        if len(members) != len(data.member_ids):
            raise ValueError("Some member IDs are invalid")

        # For PRIVATE, name is optional, for GROUP required
        if data.type == "GROUP" and not data.name:
            raise ValueError("Group conversations must have a name")

        conversation = Conversation(
            name=data.name,
            avatar=data.avatar,
            type=data.type,
            owner_id=creator_id if data.type == "GROUP" else None,
        )

        db.add(conversation)
        await db.flush()  # Get conversation.id

        # Add members
        for user in members:
            await db.execute(
                conversation_members.insert().values(
                    conversation_id=conversation.id,
                    user_id=user.id,
                    last_read_message_id=None,
                )
            )

        # For GROUP, add creator as admin
        if data.type == "GROUP":
            admin = ConversationAdmins(
                conversation_id=conversation.id, user_id=creator_id, role="LEADER"
            )
            db.add(admin)

        await db.commit()

        # Re-fetch conversation with relationships
        q = (
            select(Conversation)
            .options(
                selectinload(Conversation.members),
                selectinload(Conversation.owner),
                selectinload(Conversation.admins),
                selectinload(Conversation.last_message),
            )
            .where(Conversation.id == conversation.id)
        )
        res = await db.execute(q)
        return res.scalar_one()

    @staticmethod
    async def update(db, conversation: Conversation, data: UpdateConversation):
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(conversation, field):
                setattr(conversation, field, value)

        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    @staticmethod
    async def delete(db, conversation: Conversation):
        await db.delete(conversation)
        await db.commit()


crud_conversation = CRUDConversation()
