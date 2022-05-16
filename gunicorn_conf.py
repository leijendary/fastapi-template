from app.core.configs.app_config import app_config
from app.core.configs.security_config import security_config

_app_config = app_config()
_security_config = security_config()

bind = f"0.0.0.0:{_app_config.port}"
workers = _app_config.workers
certfile = _security_config.ssl_certfile
keyfile = _security_config.ssl_keyfile
