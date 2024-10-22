# main.py

from data_extractor import extract_data
from card_builder import CardBuilder, PDFGridBuilder, DPI

CARDS_DATA_PATH = "cards text/rat_heist.md"

# What this app does???
# "parse" data from text/markdown file into Card objects
# use list of card objects to generate Card images with PIL
# create a4 pages with card images as print sheets for real cards

def main():
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