# Simple RBAC helper
ROLE_PERMISSIONS = {
    'admin': ['*'],
    'manager': ['read', 'write', 'approve'],
    'user': ['read']
}

def has_permission(role: str, perm: str) -> bool:
    if role not in ROLE_PERMISSIONS:
        return False
    perms = ROLE_PERMISSIONS[role]
    return '*' in perms or perm in perms