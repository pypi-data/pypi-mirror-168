from .Server import QRContext


def role_manager(default_role='guest'):
    def decorator(f):
        def wrapper(ctx: QRContext, *args, **kwargs):
            role = kwargs.get('role')
            if role is None:
                role = default_role
            else:
                kwargs.pop('role')

            ctx.repository.set_role(role)
            return f(ctx, *args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    return decorator