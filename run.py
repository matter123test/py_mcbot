import asyncio

from src.bot import main
from src.logger import Logger

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Logger.log("Bot has been closed!")
