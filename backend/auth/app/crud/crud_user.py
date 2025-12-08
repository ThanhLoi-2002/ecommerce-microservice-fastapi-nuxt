from sqlalchemy import select, update
from app.db.models.user import User
from app.schemas.user import CreateUserDto
from app.utils.hashPass import HashHelper


class CRUDUser:
    @staticmethod
    async def get_one(db, filters: dict):
        q = select(User)

        for field, value in filters.items():
            if hasattr(User, field):
                q = q.where(getattr(User, field) == value)

        res = await db.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db, data: CreateUserDto):
        user = User(
            **data.model_dump(exclude={"password"}),
            password=HashHelper.get_password_hash(data.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db, user: User, data: dict):
        for field, value in data.items():
            if hasattr(User, field):
                setattr(user, field, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_by_id(db, user_id: int, data: dict):
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )

        result = await db.execute(stmt)
        await db.commit()

        return result.fetchone()


crud_user = CRUDUser()
