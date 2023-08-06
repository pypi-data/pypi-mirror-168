from src.__main__ import main

try:
    from api.command import *
    from api.config import *
except Exception as e:
    from src.api.command import *
    from src.api.config import *

if __name__ == "__main__":
    main()
