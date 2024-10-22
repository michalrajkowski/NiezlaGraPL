# Extracts data from .txt and .md card files and turns them into python dicts or json objects. 
# It is used for rapid card building and developing
from card import Card


# Read card data line by line
# Extract data from it and insert it into particular cathegories?
# Open the file in read mode

def extract_data(file_name):
    # Open data file and read data line by line
    # ### - new card data (we found the name)
    # --- - end of card data (we found the ending line)
    all_cards_data = []
    with open(file_name, 'r') as file:
        this_card : Card = None
        for line in file:
            # pseudo switch case that decides what to do with readed lines
            if line.strip().startswith("###"):
                this_card = Card.blank_card()
                this_card.name = line.strip("### ")
                all_cards_data.append(this_card)
            elif line.strip().startswith("---"):
                # load art
                this_card.art = 'assets/arts/default_art.png'
            else:
                this_card.text+=line
    return all_cards_data