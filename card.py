# card.py — the Card class and the raw data the deck is built from.
#
# Import direction matters: deck.py imports from card.py, never the reverse.
# Cards know nothing about decks. If card.py ever needs something from deck.py,
# that's a design smell before it's an error (Python raises on circular imports).


# ===Module level constant===
# This is value that's defined once and never reassigned while the program runs
# Basically the raw data, written with all caps
#
# ALL_CAPS is a convention, not enforcement — Python won't stop you reassigning
# these. It's a signal to a reader: "this is fixed reference data, don't touch."
# They live at module level (not inside the class) because they describe the
# tarot system itself, not any one card.
MAJOR_NAME = [
    # Order is meaningful: the list index IS the card's number, 0-21.
    # deck.py relies on this by using enumerate() to get name and number together.
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

# A list of tuples, not a flat list: each entry pairs a display name with its
# number, so the two can never drift apart. Unpacked in deck.py as
# `for rank, n in RANK` — tuple unpacking, same as enumerate() gives you.
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

# 22 Majors + (14 ranks x 4 suits) = 22 + 56 = 78. The deck's size is a
# consequence of this data, never a number typed in anywhere.


# ===Defining classes===
class Card:
    """A single tarot card. A blueprint — writing this creates no cards.

    An actual card only exists when some other code calls Card(...).
    """

    def __init__(self, name, arcana, number, suit, is_reversed=False):
        # __init__ is the initializer: Python calls it automatically every time
        # you write Card(...), passing along whatever arguments you gave.
        #
        # `self` is THIS PARTICULAR card — the one being built right now.
        # Python passes it in automatically; you never supply it yourself.
        #
        # Four required parameters because every card genuinely differs in all
        # four respects. The fifth, is_reversed, has a default: a card is upright
        # unless told otherwise, and shuffle() is what decides otherwise later.
        #
        # Contrast Deck, which takes exactly one parameter: the 78 cards are
        # identical in every deck ever built, so the only thing worth telling a
        # deck from outside is whether it reads with reversals. Parameters are
        # for what VARIES between instances.
        #
        # Each `self.x = x` line creates an instance attribute — data owned by
        # this card alone. Two cards never share them.
        self.name = name
        self.arcana = arcana
        self.number = number
        self.suit = suit  # None for Majors — they have no suit
        self.is_reversed = is_reversed

    def __str__(self):
        # Dunder ("double underscore") method: never called by name. Python calls
        # it for you when you write print(card) or str(card).
        #
        # The user-facing view — verbose and readable. Must RETURN a string;
        # a __str__ that calls print() and returns nothing crashes the moment
        # Python tries to use its result.
        return f"Card: {self.name}, Arcana type: {self.arcana}, Number: {self.number}, Suit: {self.suit}, Is reversed?: {self.is_reversed}"

    def __eq__(self, other):
        # Runs whenever you write card_a == card_b.
        #
        # Without this, == falls back to identity — "are these literally the same
        # object in memory?" — so two separately-built Fools would compare False.
        if not isinstance(other, Card):
            # Guard for being handed a string, None, an int, anything non-Card.
            # NotImplemented is a special VALUE, not an exception and not False:
            # it tells Python "I don't know how to compare with that", so Python
            # then tries the other object's __eq__ before finally deciding False.
            # Without this guard, `card == "text"` would crash on other.name.
            return NotImplemented

        # Design decision: name only. Orientation is deliberately excluded, so a
        # reversed Tower still equals an upright Tower — they're the same card,
        # just differently placed. Name alone is enough to identify a card
        # uniquely across all 78.
        return self.name == other.name

        # Side effect worth knowing: defining __eq__ silently makes Card
        # unhashable — cards can't go in a set() or be dict keys until __hash__
        # is defined too. Only matters if a set of cards is ever needed.

    def __repr__(self):
        # The debugging view, deliberately compact. Python uses __repr__ (not
        # __str__) for objects sitting INSIDE a container — which is why
        # printing a list of cards shows this short form, not the long one above.
        # That's what makes `print(deck.packed_cards)` readable at 78 cards.
        return f"{self.number} - {self.name}"


# --- test ---
# Phase 1-2 scratch work, kept as a record of what was verified.
# Commented out because any bare code at module level runs on IMPORT — deck.py
# does `from card import ...`, which executes this whole file top to bottom.
# Uncommented, these would print every time the deck is built. The permanent
# fix for that is an `if __name__ == "__main__":` guard, as used in deck.py.
# Orientation is a boolean now, so the 5th argument is False/True — and since it
# defaults to False, the upright cards can simply leave it off entirely.
# card0 = Card("The Fool", "Major Arcana", 0, None)
# copy_card0 = Card("The Fool", "Major Arcana", 0, None)
# rev_card0 = Card("The Fool", "Major Arcana", 0, None, True)
# ncard = "not card"
# print(card0.name)
# print(card0.arcana)
# print(card0.number)
# print(card0.suit)
# print(card0.is_reversed)
# print(card0)
# print(card0 == copy_card0)      # True  — same name, separate objects
# print(rev_card0 == card0)       # True  — orientation excluded by design
# print(ncard == card0)           # False — the isinstance guard handles it
