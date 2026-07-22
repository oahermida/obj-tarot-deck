# spread.py — the Spread class and the spread definitions. (Phase 7)
#
# A Spread knows its name, its ordered position labels (Past / Present / Future
# to start with, Celtic Cross later), and — once performed — which drawn card
# sits in which position.
#
# This is the composition phase: a Spread HAS Cards, it isn't one. It also
# doesn't own a Deck — it borrows one, taking it as an argument to the method
# that performs the reading. Which spreads exist should be data, so adding the
# Celtic Cross later means adding data, not writing a second class.
#
# Imports point one way: spread imports from deck and card, never the reverse.
