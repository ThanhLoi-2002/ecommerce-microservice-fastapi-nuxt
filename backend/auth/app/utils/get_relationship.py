from sqlalchemy.orm import selectinload
from typing import List, Type, Any

def get_relationship_options(relationship_names: List[str], model: Type[Any]) -> List:
    relationship_map = {
        'members': model.members,
        'owner': model.owner,
        'admins': model.admins,
        'last_message': model.last_message,
    }

    options = []
    for relationship in relationship_names:
        if relationship in relationship_map:
            options.append(selectinload(relationship_map[relationship]))
    
    return options