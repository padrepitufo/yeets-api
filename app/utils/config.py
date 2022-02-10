import os


def _get(var: str, default: str = "", required=False) -> str:
    env_var = os.getenv(key=var)
    if required and not env_var:
        raise SystemExit(f"missing environment variable ({var}) exiting...")
    return env_var or default


_HOST = _get("DATABASE_HOST")
_NAME = _get("DATABASE_NAME")
_PASS = _get("DATABASE_PASS")
_USER = _get("DATABASE_USER")
DATABASE_URL = f"mysql://{_USER}:{_PASS}@{_HOST}:3306/{_NAME}"
DEBUG = bool(int(_get("DEBUG", default="0", required=False)))
ENVIRONMENT = _get("ENVIRONMENT")
LOG_LEVEL = _get("LOG_LEVEL", default="DEBUG", required=False)
LOG_FORMAT = _get(
    "LOG_FORMAT",
    default="%(levelname)s:%(asctime)s [%(filename)s:%(lineno)d] %(message)s",
    required=False,
)