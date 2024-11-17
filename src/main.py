# main.py

from data_extractor import extract_data
from card_builder import CardBuilder,PlayerCardBuilder,DungeonCardBuilder, PDFGridBuilder, DPI
from card import Card, CardColor, Stats

CARDS_DATA_PATH = "cards text/rat_heist.md"

# What this app does???
# "parse" data from text/markdown file into Card objects
# use list of card objects to generate Card images with PIL
# create a4 pages with card images as print sheets for real cards

def main():
    print("ok")
    # mock card data
    # test card building on mocked data
    mocked_card = Card(
        name="Test Card",
        art = "assets/arts/default_art.png",
        text = "Example description/n 123 123 123 123",
        color=CardColor.YELLOW,
        cost={CardColor.RED: 1, CardColor.BLUE: 1, CardColor.NONE: 1},
        stats=Stats(hp=2, attack=3, cards=1)
    )
    card_builder : CardBuilder = DungeonCardBuilder(mocked_card)
    card_image = card_builder.build_card()
    card_image.show()
    pass

def build_cards_from_path():
    cards_list = extract_data(CARDS_DATA_PATH)
    card_images = []
    for card_data in cards_list:
        builder = CardBuilder(card_data)
        card_image = builder.build_card()
        card_images.append(card_image)

    # Build the grid and save it as a PDF
    grid_builder = PDFGridBuilder(card_images)
    grid_builder.save_as_pdf("output/cards_grid.pdf")

if __name__ == "__main__":
    main()