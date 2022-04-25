from app.core.configs.app_config import app_config
from app.core.configs.security_config import security_config

_config = app_config()
_security = security_config()

bind = f"0.0.0.0:{_config.port}"
workers = _config.workers
certfile = _security.ssl_certfile
keyfile = _security.ssl_keyfile
