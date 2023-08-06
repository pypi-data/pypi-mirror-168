from .admin.views import bp as admin_bp
from .pos.views import pos as pos_bp
from .user.views import user as user_bp
from .core.views import core as core_bp

blueprints = [
    core_bp,
    user_bp,
    pos_bp,
    admin_bp
]
