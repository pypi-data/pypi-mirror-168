from os import environ
from .exceptions import MustBeOnReplit

class Links:
    """bot urls (docs)"""
    def __init__(self) -> None:
        if ("REPL_SLUG" not in environ or
            "REPL_OWNER" not in environ or
            "REPLIT_DB_URL" not in environ):
                raise MustBeOnReplit("Currently, you must be on replit to run this. Thanks! Local support is WIP")
        self.docs: str = f"https://{environ['REPL_SLUG']}.{environ['REPL_OWNER']}.repl.co"

links = Links()