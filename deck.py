from card import MAJOR_NAME, RANK, SUIT, Card


# ===Defining class===
class Deck:
    def __init__(self):
        self.packed_cards = []
        for n, card in enumerate(MAJOR_NAME):
            self.packed_cards.append(Card(card, "Major Arcana", n, None, "Upright"))
        for rank, n in RANK:
            for suit in SUIT:
                self.packed_cards.append(
                    Card(f"{rank} of {suit}", "Minor Arcana", n, suit, "Upright")
                )


if __name__ == "__main__":
    deck = Deck()
    print(deck.packed_cards)
