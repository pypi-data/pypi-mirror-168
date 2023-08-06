from typing import List, Optional

__version__ = "1.5.0"

def main(args: Optional[List[str]] = None) -> int:
    from invokescons.command_line import main as _main
    return _main()
