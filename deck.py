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

    def __init__(self, reversals=False):
        # One parameter beyond self, and exactly one: whether this deck reads
        # with reversals. That's the only thing that genuinely differs between
        # two decks — the 78 cards themselves are identical in every deck ever
        # built, so they get constructed in here rather than passed in.
        # Parameters are for what VARIES per instance; what's always the same
        # belongs in the body.
        #
        # Defaults to False, so a plain Deck() still works and reads
        # upright-only — reversals are opt-in.

        # The deck's own list of cards. Starts empty and gets filled below.
        self.packed_cards = []

        self.reversals = reversals

        # --- The 22 Majors ---
        # enumerate() yields (index, item) pairs, and here the index IS the
        # card's number — which only works because MAJOR_NAME is in ritual order.
        # `n` is the counter, `card` is the name string from the list.
        for n, card in enumerate(MAJOR_NAME):
            # Each Card(...) call builds one new object; .append() puts it in
            # this deck's list. 22 separate cards, none of them sharing state.
            # suit is None (Majors have no suit); is_reversed starts False,
            # which is correct rather than a placeholder — a fresh, unshuffled
            # deck genuinely is all upright. shuffle() decides the real values.
            self.packed_cards.append(Card(card, "Major Arcana", n, None, False))

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
                    Card(f"{rank} of {suit}", "Minor Arcana", n, suit, False)
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

        # --- The orientation pass ---
        # Design decision: orientation is decided HERE, at shuffle time, not at
        # draw time. The alternative would leave every undrawn card carrying an
        # orientation that means nothing until it's drawn — the object would be
        # lying about its own state. Assigning here means all 78 always hold a
        # real value. (Cost accepted: a method named "shuffle" now does two
        # jobs. Defensible because in actual practice the shuffle IS when cards
        # get turned around.)
        #
        # Note the loops assign to card.is_reversed directly. `card` isn't a
        # copy or an index — it's a reference to the very object in the list, so
        # the dot reaches through and the list sees the change.
        #
        # The invariant this maintains: after shuffle() returns, the deck's
        # orientations always match the deck's own reversals setting. That's why
        # the else branch below FORCES upright rather than skipping the pass —
        # skipping would let stale reversed cards survive a flag change, and
        # nothing stops the flag changing (Python has no `private`).
        #
        # Both branches must write on every path. A branch that skips the
        # assignment doesn't leave the card neutral, it leaves the card's
        # PREVIOUS value in place — which turns the coin flip into a one-way
        # ratchet that converges on all-reversed after a few shuffles.
        if self.reversals == True:
            for card in self.packed_cards:
                reverse = random.randint(0, 1)
                if reverse == 1:
                    card.is_reversed = True
                else:
                    card.is_reversed = False
        else:
            for card in self.packed_cards:
                card.is_reversed = False

    def draw(self):
        # A guard clause: handle the bad case up front and bail out, so the
        # normal path below reads flat instead of nested inside an else.
        #
        # Design decision: raise rather than return a sentinel like None.
        # Drawing from an empty deck is a CALLER bug — a three-card spread asking
        # a 78-card deck for cards can only run dry if something upstream is
        # already broken — and bugs should be loud. A None would travel silently
        # until it hit an attribute access several lines away, far from the cause.
        #
        # The check has to come before the pop; popping first would crash before
        # the guard ever ran. raise exits the method immediately, which is why
        # there's no else.
        #
        # An empty list.pop() already raises IndexError on its own, so the two
        # extra lines aren't buying the exception — they're buying the MESSAGE.
        # Python's default reads "pop from empty list", which talks about this
        # deck's internal storage; a caller has no business knowing a Deck has a
        # list inside it. IndexError is reused deliberately: it's the built-in
        # that already means "asked a sequence for something that isn't there".
        if not self.packed_cards:
            raise IndexError("There is no deck to draw from. Build a deck first.")

        # pop() does two things in one call — removes the card AND hands it
        # back — which is exactly what drawing means.
        #
        # No argument, so it takes the LAST item: the end of the list is "the top
        # of the deck". pop(0) would take the first and read more like dealing off
        # a physical deck, but it has to shift all 77 remaining elements down one
        # position (O(n)) where popping the end is O(1). Unmeasurable at 78 cards
        # either way — chosen for the cheaper operation, not for meaning.
        drawn_card = self.packed_cards.pop()

        # Unlike shuffle(), this one DOES return. shuffle() changes the deck the
        # caller already holds, so there's nothing to hand back; draw() gives
        # them a card they didn't have before.
        #
        # Note what's absent: nothing here touches orientation. That was decided
        # at shuffle time. Reaching for random in this method would mean the
        # shuffle-time decision had leaked.
        return drawn_card


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

    print("Testing drawing:")
    draw1 = deck.draw()
    deck.shuffle()
    print(deck.packed_cards)
    draw2 = deck.draw()
    deck.shuffle()
    draw3 = deck.draw()

    print(f"You drew: {draw1.name}, {draw2.name} and {draw3.name}")
    print(f"Leftover cards:{len(deck.packed_cards)}")

    try:
        current_n_cards = len(deck.packed_cards)
        for card in range(current_n_cards):
            card = deck.draw()
        deck.draw()
    except IndexError:
        print("There is no deck to draw from. Build a deck first.")
