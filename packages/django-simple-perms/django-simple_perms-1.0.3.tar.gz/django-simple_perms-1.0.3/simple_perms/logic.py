from .settings import SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION


class PermissionLogic:
    def default_permission(self, user, obj, perm):
        return SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION(user, obj, perm)
