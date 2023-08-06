_registry = {}


def register(app_label, logic_class):
    if app_label in _registry:
        raise AttributeError(
            f'The "{app_label}" app is already registerd by simple_perms'
        )
    _registry[app_label] = logic_class()


def get_app_logic(app_label):
    return _registry.get(app_label, None)
