# Extracts data from .txt and .md card files and turns them into python dicts or json objects. 
# It is used for rapid card building and developing
from card import Card, CardColor
from abc import ABC, abstractmethod

# Extractor class will extract card data from txt file and change it to list of card data format?
# TODO: Json extractor?
# TODO: serialized python object loading?
class AbstractExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract_data(file_name):
        pass

class BaseExtractor(AbstractExtractor):
    def extract_color(self, line: str, card: Card) -> bool:
        '''
        Try to extract card color from text in any format:
        - Full name: e.g., "red", "green", "blue"
        - Short name: e.g., "r", "g", "b"
        
        Returns True if the color is successfully extracted, False otherwise.
        '''
        line = line.strip().lower()

        # Mapping for full color names to CardColor enum
        full_color_map = {
            "red": CardColor.RED,
            "green": CardColor.GREEN,
            "blue": CardColor.BLUE,
            "yellow": CardColor.YELLOW,
            "purple": CardColor.PURPLE,
            "none": CardColor.NONE
        }

        # Mapping for short color codes to CardColor enum
        short_color_map = {
            "r": CardColor.RED,
            "g": CardColor.GREEN,
            "b": CardColor.BLUE,
            "y": CardColor.YELLOW,
            "p": CardColor.PURPLE,
            "n": CardColor.NONE
        }

        # Try to match with full color name
        if line in full_color_map:
            card.color = full_color_map[line]
            return True

        # Try to match with short color code
        elif line in short_color_map:
            card.color = short_color_map[line]
            return True

        # If no match, return False and don't change the card color
        return False
     
    def extract_stats(self, line, card:Card) -> bool:
        '''

        '''
        return False
    def extract_data(self, file_name):
        '''
        change data from text file into a list of Card objects.
        Automaticly extracts and cathegorise variables from simple text form
        Text data of each card should be in below format (ignore tabulation, it is for readability):
            ### Name
            <Color>
            <Symbols>

            <Multiline description>

            ---
            <empty line>
        '''
        all_cards_data = []
        with open(file_name, 'r') as file:
            this_card : Card = None
            found_name = False
            for line in file:
                if found_name:
                    # try to extract color or stats
                    if (self.extract_color(line,this_card)):
                        continue
                    if (self.extract_stats(line, this_card)):
                        continue
                    found_name=False

                if line.strip().startswith("###"):
                    this_card = Card.blank_card()
                    this_card.name = line.strip("### ")
                    all_cards_data.append(this_card)
                    found_name = True
                elif line.strip().startswith("---"):
                    # This means that we fund the card end! We will wait for the next card name now to create now card?
                    # On end operations:
                    this_card.art = ''
                else:
                    this_card.text+=line
        return all_cards_data

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