# deck.py — the Deck class: builds all 78 cards, shuffles, and (later) draws.
#
# Imports point one way only: deck knows cards, cards don't know decks.

import random

# Anything this file uses by name must be imported. Being defined in card.py
# doesn't make a name visible here — the import line doubles as a readable list
# of everything deck.py depends on.
from card import MAJOR_NAME, RANK, SUIT, Card


# ===Defining class===
class Deck:
    """A full 78-card tarot deck. A blueprint, exactly as Card was one.

    Writing this class creates no deck. An actual deck object only exists once
    other code calls Deck() — see the __main__ block at the bottom.
    """

    def __init__(self):
        # No parameters beyond self: every fresh tarot deck is identical, so
        # there's nothing a caller needs to tell it. What always stays the same
        # gets built inside; parameters are only for what varies per instance.

        # The deck's own list of cards. Starts empty and gets filled below.
        self.packed_cards = []

        # --- The 22 Majors ---
        # enumerate() yields (index, item) pairs, and here the index IS the
        # card's number — which only works because MAJOR_NAME is in ritual order.
        # `n` is the counter, `card` is the name string from the list.
        for n, card in enumerate(MAJOR_NAME):
            # Each Card(...) call builds one new object; .append() puts it in
            # this deck's list. 22 separate cards, none of them sharing state.
            # suit is None (Majors have no suit); every card starts Upright.
            self.packed_cards.append(Card(card, "Major Arcana", n, None, "Upright"))

        # --- The 56 Minors ---
        # Nested loop: the outer runs 14 times (once per rank), and for EACH of
        # those the inner runs 4 times (once per suit). 14 x 4 = 56 cards.
        #
        # `for rank, n in RANK` unpacks each tuple as it goes: ("Ace", 1) puts
        # "Ace" in rank and 1 in n.
        for rank, n in RANK:
            for suit in SUIT:
                self.packed_cards.append(
                    # The name is composed rather than typed out — no card
                    # written twice anywhere in this project.
                    Card(f"{rank} of {suit}", "Minor Arcana", n, suit, "Upright")
                )

        # Rank-major ordering (all four Aces, then all four Twos...) rather than
        # suit-major (all Wands, then all Cups...). Purely cosmetic — the deck
        # gets shuffled anyway. Swapping the two loop lines would flip it.

    def shuffle(self):
        # A method: an ordinary function that lives on the class and takes the
        # instance as its first parameter.
        #
        # `deck.shuffle()` is syntactic sugar — Python rewrites it as
        # `Deck.shuffle(deck)`, passing the object left of the dot in as `self`.
        # That's why self must be here to catch it, and why this is called with
        # dot notation (deck.shuffle()) rather than as a bare shuffle(deck).
        #
        # self.packed_cards, not deck.packed_cards: `self` means "whichever deck
        # I'm running on right now". Naming a specific deck here would work
        # by accident with one deck and silently break with two.
        #
        # No return statement, deliberately. random.shuffle() reorders the list
        # IN PLACE and evaluates to None — it does not hand back a new list.
        # There's nothing meaningful to return, because the caller already
        # reaches the reordered cards through the deck object itself.
        random.shuffle(self.packed_cards)


# This block runs only when deck.py is executed directly (python3 deck.py).
# On `import deck` it's skipped — which is what keeps test code from firing
# every time another module imports this one.
if __name__ == "__main__":
    # Calling the class is what actually builds a deck. Class in deck.py,
    # instance created here.
    deck = Deck()

    print(deck.packed_cards)  # 78 cards, in build order (uses Card.__repr__)
    print(len(deck.packed_cards))  # 78 — currently via the list; Phase 4 makes
    #      len(deck) work directly, via __len__

    # Two separate statements: shuffle() returns nothing, so there's no value to
    # print. Call it for the effect, then look at what changed.
    # (print(deck.shuffle()) would just print None.)
    deck.shuffle()
    print(deck.packed_cards)  # same 78 cards, genuinely different order
