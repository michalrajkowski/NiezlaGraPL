# Card elements:
from enum import Enum, auto

class CardColor(Enum):
    # Player Cards Colors
    NONE = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    PURPLE = auto()
    # Dungeon Colors
    DUNGEON = auto()


class Stats:
    def __init__(self, hp: int = 0, attack: int = 0, cards: int = 0):
        # Initialize stats with default values
        self.hp = hp
        self.attack = attack
        self.cards = cards

        # Define the emote dict
        self.emote_dict = {
            'hp': '❤️',       # Heart emoji for HP
            'attack': '⚔️',    # Crossed swords emoji for attack
            'cards': '🃏'      # Joker emoji for cards
        }

    def stats_to_string(self):
        """Convert stats to a string representation, ignoring 0 values."""
        stats = {}
        if self.hp > 0:
            stats[self.emote_dict['hp']] = self.hp
        if self.attack > 0:
            stats[self.emote_dict['attack']] = self.attack
        if self.cards > 0:
            stats[self.emote_dict['cards']] = self.cards

        # Build a string with the remaining stats
        stat_strings = [f"{key}:{value}" for key, value in stats.items()]
        return ' | '.join(stat_strings)
        

class Card:
    def __init__(self, name, art, text, color:CardColor=CardColor.NONE, cost=None, stats:Stats=None):
        self.name = name
        self.art = art
        self.text = text
        self.color = color
        self.cost = cost or {CardColor.NONE: 0}
        self.stats = stats or Stats()

    @classmethod
    def from_defaults(cls):
        return cls(name="Default Name", art="Default Art", text="Default Text")
    
    @classmethod
    def blank_card(cls):
        return cls(name="", art="", text="")

    def __repr__(self):
        return f"<Card(name={self.name}, attack={self.art}, defense={self.text})>"
