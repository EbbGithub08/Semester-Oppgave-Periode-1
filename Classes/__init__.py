"""
Classes package for game entities (Player, Button, etc.).

Gjør det mulig å importere direkte fra `Classes`, f.eks.:
    from Classes import Player, World, HighscoreDatabase
"""

from .player import Player
from .button import Button
from .database import HighscoreDatabase
from .world import World
from .others import Enemy, Platform, Lava, Coin, Exit, Spike

__all__ = [
    "Player",
    "Button",
    "HighscoreDatabase",
    "World",
    "Enemy",
    "Platform",
    "Lava",
    "Coin",
    "Exit",
    "Spike",
]

