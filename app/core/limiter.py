from slowapi import Limiter
from slowapi.util import get_remote_address
import os

is_testing = os.getenv("TESTING", "false").lower() == "true"

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not is_testing,
)