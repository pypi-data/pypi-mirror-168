from typing import Literal

ParseModes = Literal["MarkdownV2", "HTML"]

Dices = Literal[
    "🎲", "🎯", "🎳",  # Can result in values from 1 to 6
    "🏀", "⚽",  # Can result in values from 1 to 5
    "🎰"  # Can result in values from 1 to 64
]
