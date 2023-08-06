from .registry import get_app_logic
from .settings import SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION


class PermissionBackend:
    def has_perm(self, user, perm, obj=None):
        try:
            app_label, perm_name = perm.split(".")
        except Exception as e:
            raise AttributeError(
                f'The given perm attribute "{perm}" hasn\'t the required format : '
                '"app_label.permission_name"'
            ) from e

        logic = get_app_logic(app_label)

        if logic:
            if hasattr(logic, perm_name):
                return getattr(logic, perm_name)(user, obj, perm)

            return logic.default_permission(user, obj, perm)

        return SIMPLE_PERMS_GLOBAL_DEFAULT_PERMISSION(user, obj, perm)

    def authenticate(self, *args):
        return None
