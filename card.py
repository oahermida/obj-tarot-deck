# ===Module level constant===
# This is value that's defined once and never reassigned while the program runs
# Basically the raw data, written with all caps
MAJOR_NAME = [
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit",
    "Wheel of Fortune",
    "Justice",
    "The Hanged Man",
    "Death",
    "Temperance",
    "The Devil",
    "The Tower",
    "The Star",
    "The Moon",
    "The Sun",
    "Judgement",
    "The World",
]
SUIT = ["Wands", "Cups", "Swords", "Pentacles"]
RANK = [
    ("Ace", 1),
    ("Two", 2),
    ("Three", 3),
    ("Four", 4),
    ("Five", 5),
    ("Six", 6),
    ("Seven", 7),
    ("Eight", 8),
    ("Nine", 9),
    ("Ten", 10),
    ("Knight", 11),
    ("Queen", 12),
    ("King", 13),
    ("Page", 14),
]  # Design decision: simplicity over qabalistic accuracy — pips 1-10 in order, then courts as Knight 11, Queen 12, King 13, Page 14 (my order, not RWS's Page-first)


# ===Defining classes===
class Card:
    def __init__(self, name, arcana, number, suit, orientation):
        self.name = name
        self.arcana = arcana
        self.number = number
        self.suit = suit
        self.orientation = orientation

    def __str__(self):
        return f"Card: {self.name}, Arcana type: {self.arcana}, Number: {self.number}, Suit: {self.suit}, Orientation: {self.orientation}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"{self.number} - {self.name}"


# --- test ---
# card0 = Card("The Fool", "Major Arcana", 0, None, "Upright")
# copy_card0 = Card("The Fool", "Major Arcana", 0, None, "Upright")
# rev_card0 = Card("The Fool", "Major Arcana", 0, None, "Reversed")
# ncard = "not card"
# print(card0.name)
# print(card0.arcana)
# print(card0.number)
# print(card0.suit)
# print(card0.orientation)
# print(card0)
# print(card0 == copy_card0)
# print(rev_card0 == card0)
# print(ncard == card0)
