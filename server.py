import asyncio
from classes.game import Game
from rules_init import LORRules



async def main():
    game = Game(rules=LORRules)
    game.test_environment()
    # await game.game_looper()
    # game.game_start()


asyncio.run(main())