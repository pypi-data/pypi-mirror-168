"""file that stores the Param for type hints

```py
@bot.command(...)
def name(ctx, pass_obj: Param(
    desc="something to pass",
    required=False,
    default="lol"
)):
    ctx.post(f"@{ctx.author} {pass_obj}")
```
"""

from .exceptions import NonRequiredParamsMustHaveDefault
from typing import Any

class Param:
    """similar to discord.py param type hinting for commands"""
    def __init__(self, desc: str = "", required: bool = None, default: Any = None, type_cast = None) -> None:
        """init"""
        self.desc = desc
        self.required = required
        self.default = default
        self.type_cast = type_cast
        if (not self.required and self.default is None):
            raise NonRequiredParamsMustHaveDefault("no required params must have default")