# /// pyproject
# [project]
# name = "name"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = "==3.11.2"
#
# dependencies = [
#     "pygame-ce",
#     "pyscroll",
#      "pytmx",
#       "tool",
# ]
# ///

import pygame
import asyncio
from game import Game
from entities import player_instances

pygame.init()

if __name__ == "__main__":
    game: Game = Game()
    asyncio.run(game.run(player_instances))
