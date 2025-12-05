from app.modules.user.userModel import User
from .dto.userValidatorDto import CreateUserDto
from ...core.baseService import BaseService


class UserService(BaseService):
    def create(self, data: CreateUserDto):
        newUser = User(**data.model_dump(exclude_none=True))
        self.session.add(instance=newUser)
        self.session.commit()
        self.session.refresh(instance=newUser)

        return newUser

    def get_one(self, filters: dict):
        return self.session.query(User).filter_by(**filters).first()
    

