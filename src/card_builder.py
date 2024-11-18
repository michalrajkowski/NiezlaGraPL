from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from card import Card, CardColor
from fpdf import FPDF
from emoji_handler import multi_cost_to_emoji_text
from text_box import text_box
from emoji_text_box import emoji_text_box
# Constants
DPI = 300  # Dots per inch
CM_TO_INCH = 2.54
SYMBOLA_FONT_PATH = "fonts/Symbola/Symbola.ttf"

# Convert centimeters to pixels at 300 DPI
def cm_to_px(cm, dpi=DPI):
    return int((cm / CM_TO_INCH) * dpi)
def tuple_cm_to_px(dimension_box, dpi=DPI):
    return tuple(cm_to_px(x) for x in dimension_box)

def centered_text_position_in_box(font, text, box):
    font_width, font_height = font.getsize(text)
    new_width = box[0] + (box[2] - box[0] - font_width) / 2
    new_height = box[1] + (box[3] - box[1] - font_height) / 2
    return (int(new_width), int(new_height))

class CardBuilder:
    def __init__(self, card : Card, card_size_cm=(6.3, 8.8)):
        # Convert card size from cm to pixels
        self.card_size_cm = card_size_cm
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.card = card
    
    def percent_tuple_to_px(self, percent_tuple, symmetry_x=False, symmetry_y=False):
        (percent_x1, percent_y1, percent_x2, percent_y2) = percent_tuple
        card_width, card_height = self.card_size_px  # Assuming self.card_size_px is (width, height)

        # Calculate x and y positions
        px_x1 = percent_x1 * card_width
        px_y1 = percent_y1 * card_height

        # Calculate width and height with optional symmetry
        px_x2 = card_width - px_x1 if symmetry_x else  percent_x2 * card_width 
        px_y2 = card_height - px_y1 if symmetry_y else  percent_y2 * card_height

        return (px_x1, px_y1, px_x2, px_y2)
        

    def build_card(self):
        # load fonts
        try:
            font = ImageFont.truetype(SYMBOLA_FONT_PATH, 60)
        except IOError:
            print("Symbola font not found, falling back to default font.")
            font = ImageFont.load_default()

        # Very simple builder:
        # Insert Name box
        # Description box
        # Art

        # New blank rectangle
        
        # Add interior color?
        
        # Add 

        # Open a card template or create a blank card
        
        card_image = Image.new(mode="RGB", size=self.card_size_px)
        draw = ImageDraw.Draw(card_image)

        # Inner color
        draw.rectangle((cm_to_px(0.3), cm_to_px(0.3), self.card_size_px[0]-cm_to_px(0.3), self.card_size_px[1]-cm_to_px(0.3)), 
                        fill ="red", outline ="red")
        # Draw art
        art_box_cm = (0.5, 1.0, 6.3-1.0, 4.0)
        art_box_px = (cm_to_px(art_box_cm[0]),cm_to_px(art_box_cm[1]),cm_to_px(art_box_cm[2]),cm_to_px(art_box_cm[3]))
        card_art = Image.open(self.card.art).resize((art_box_px[2], art_box_px[3]), resample=Image.Resampling.NEAREST)
        card_image.paste(card_art, (art_box_px[0], art_box_px[1]))

        # Draw name box and description box
        # Name
        draw.rectangle((cm_to_px(0.5), cm_to_px(0.5), cm_to_px(self.card_size_cm[0] - 0.5), cm_to_px(0.5+0.5)), 
                        fill ="white", outline ="black")
        # Description     
        draw.rectangle((cm_to_px(0.5), cm_to_px(5.0), cm_to_px(self.card_size_cm[0] - 0.5), cm_to_px(8.0)), 
                        fill ="white", outline ="black")

        # Draw text (name, attack, defense, description)
        draw.text((cm_to_px(0.5), cm_to_px(0.5)), self.card.name, font=font, fill=(0, 0, 0))
        with Pilmoji(card_image) as pilmoji:
            pilmoji.text((cm_to_px(0.5), cm_to_px(4.4)), self.card.text, (0, 0, 0), font)
        # draw.text((20, 40), self.card.text, font=font, fill=(0,0,0))

        return card_image

# This is actualy not a blank card but player card
class PlayerCardBuilder(CardBuilder): 
    def __init__(self, card : Card, card_size_cm=(6.3, 8.8)):
        # Convert card size from cm to pixels
        self.card_size_cm = card_size_cm
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.card = card
    
    # Method for building card image
    # We might want to add some OOP here in the future so card building process is maybe more modular?
    #   Or we add building same as UI elements with flow layouts etc
    def build_card(self):
        # Load card Fonts
        # try:
        #    font = ImageFont.truetype(SYMBOLA_FONT_PATH, 32)
        #except IOError:
        #    print("Symbola font not found, falling back to default font.")
        #    font = ImageFont.load_default()
        # font = ImageFont.load_default()
        emote_font = ImageFont.truetype(SYMBOLA_FONT_PATH, 60)
        description_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 30)
        name_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 40)
        '''
        UI for player cards:
        + card type border - card color (color)
        - set symbol / release symbol for easier sorting (right bottom corner?)
        - name
        - Cost
        - effect
        - temp art maybe
        - description box 
        '''

        def card_color_enum_to_hex_color(card_color_enum : CardColor) -> str:
            match card_color_enum:
                case CardColor.NONE:
                    return "rgb(255,255,255)"
                case CardColor.RED:
                    return "rgb(255,0,0)"
                case CardColor.GREEN:
                    return "rgb(0,255,0)"
                case CardColor.BLUE:
                    return "rgb(0,0,255)"
                case CardColor.YELLOW:
                    return "rgb(255,255,0)"
                case CardColor.PURPLE:
                    return "rgb(128,0,128)"
                case CardColor.DUNGEON:
                    return "rgb(67,99,75)"

        
        card_image = Image.new(mode="RGB", size=self.card_size_px)
        draw = ImageDraw.Draw(card_image)
        # card border color
        # Inner color
        card_color_enum = self.card.color
        card_color = card_color_enum_to_hex_color(card_color_enum)

        # Draw boxes for each card Parts? (name box, description box, cost box, art box, Set/sort box?)
        # Draw art
        WHOLE_CARD_BOX = (0.00, 0.00, 1.00, 1.00)
        whole_card_box = self.percent_tuple_to_px(WHOLE_CARD_BOX, False, False)
        draw.rectangle(whole_card_box,fill="black",outline ="red")

        COLOR_BOX = (0.05, 0.03, 1.00, 1.00)
        color_box = self.percent_tuple_to_px(COLOR_BOX, True, True)
        draw.rectangle(color_box,fill=card_color,outline ="red")
        
        INNER_WHITE_BOX = (0.1, 0.1, 1.0, 1.0)
        inner_white_box = self.percent_tuple_to_px(INNER_WHITE_BOX, True, True)
        draw.rectangle(inner_white_box,fill="white",outline ="red")

        ART_BOX = (0.1, 0.2, 1.0, 0.6)
        art_box = self.percent_tuple_to_px(ART_BOX, True, False)
        draw.rectangle(art_box,fill="blue",outline ="red")
        
        NAME_BOX = (0.1, 0.1, 1.00, 0.2)
        name_box = self.percent_tuple_to_px(NAME_BOX, True, False)
        draw.rectangle(name_box,fill=None,outline ="red")

        # Draw card name
        text = self.card.name
        name_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 40)
        font_width, font_height = name_font.getsize(text)
        new_width = name_box[0] + (name_box[2] - name_box[0] - font_width) / 2
        new_height = name_box[1] + (name_box[3] - name_box[1] - font_height) / 2
        draw.text((new_width, new_height), text, fill="black", font=name_font)

        COSTS_BOX = (0.25, 0.55, 1.0, 0.65)
        costs_box = self.percent_tuple_to_px(COSTS_BOX, True, False)
        draw.rectangle(costs_box,fill="white",outline ="black")

        # Draw costs symbols
        card_cost = self.card.cost
        cost_text = multi_cost_to_emoji_text(card_cost)
        emote_text_box = centered_text_position_in_box(emote_font, cost_text, costs_box)
        with Pilmoji(card_image) as pilmoji:
            pilmoji.text(emote_text_box, cost_text, (0, 0, 0), emote_font)

        DESCRIPTION_BOX = (0.1, 0.65, 1.00, 0.9)
        description_box = self.percent_tuple_to_px(DESCRIPTION_BOX, True, False)
        draw.rectangle(description_box,fill=None,outline ="red")

        # Card Description text:
        (x1,y1,x2,y2) = description_box
        description_box_wh = (x1, y1, x2-x1, y2-y1)
        emoji_text_box(self.card.text, card_image, description_font, description_box_wh, fill="black")
        # with Pilmoji(card_image) as pilmoji:
        #     pilmoji.text((int(description_box[0]), int(description_box[1])), self.card.text, (0, 0, 0), description_font)

        return card_image

# This is actualy not a blank card but player card
class DungeonCardBuilder(CardBuilder): 
    def __init__(self, card : Card, card_size_cm=(6.3, 8.8)):
        # Convert card size from cm to pixels
        self.card_size_cm = card_size_cm
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.card = card
    
    # Method for building card image
    # We might want to add some OOP here in the future so card building process is maybe more modular?
    #   Or we add building same as UI elements with flow layouts etc
    def build_card(self):
        # Load card Fonts
        # try:
        #    font = ImageFont.truetype(SYMBOLA_FONT_PATH, 32)
        #except IOError:
        #    print("Symbola font not found, falling back to default font.")
        #    font = ImageFont.load_default()
        # font = ImageFont.load_default()
        emote_font = ImageFont.truetype(SYMBOLA_FONT_PATH, 60)
        description_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 30)
        name_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 40)
        '''
        UI for player cards:
        + card type border - card color (color)
        - set symbol / release symbol for easier sorting (right bottom corner?)
        - name
        - Cost
        - effect
        - temp art maybe
        - description box 
        '''

        def card_color_enum_to_hex_color(card_color_enum : CardColor) -> str:
            match card_color_enum:
                case CardColor.NONE:
                    return "rgb(255,255,255)"
                case CardColor.RED:
                    return "rgb(255,0,0)"
                case CardColor.GREEN:
                    return "rgb(0,255,0)"
                case CardColor.BLUE:
                    return "rgb(0,0,255)"
                case CardColor.YELLOW:
                    return "rgb(255,255,0)"
                case CardColor.PURPLE:
                    return "rgb(128,0,128)"
        
        card_image = Image.new(mode="RGB", size=self.card_size_px)
        draw = ImageDraw.Draw(card_image)
        # card border color
        # Inner color
        card_color_enum = self.card.color
        card_color = card_color_enum_to_hex_color(card_color_enum)

        # Draw boxes for each card Parts? (name box, description box, cost box, art box, Set/sort box?)
        # Draw art
        WHOLE_CARD_BOX = (0.00, 0.00, 1.00, 1.00)
        whole_card_box = self.percent_tuple_to_px(WHOLE_CARD_BOX, False, False)
        draw.rectangle(whole_card_box,fill="black",outline ="red")

        COLOR_BOX = (0.05, 0.03, 1.00, 1.00)
        color_box = self.percent_tuple_to_px(COLOR_BOX, True, True)
        draw.rectangle(color_box,fill=card_color,outline ="red")
        
        INNER_WHITE_BOX = (0.1, 0.1, 1.0, 1.0)
        inner_white_box = self.percent_tuple_to_px(INNER_WHITE_BOX, True, True)
        draw.rectangle(inner_white_box,fill="white",outline ="red")

        ART_BOX = (0.1, 0.2, 1.0, 0.6)
        art_box = self.percent_tuple_to_px(ART_BOX, True, False)
        draw.rectangle(art_box,fill="blue",outline ="red")
        
        NAME_BOX = (0.1, 0.1, 1.00, 0.2)
        name_box = self.percent_tuple_to_px(NAME_BOX, True, False)
        draw.rectangle(name_box,fill=None,outline ="red")

        # Draw card name
        text = self.card.name
        name_font = ImageFont.truetype('fonts/GidoleFont/Gidole-Regular.ttf', 40)
        font_width, font_height = name_font.getsize(text)
        new_width = name_box[0] + (name_box[2] - name_box[0] - font_width) / 2
        new_height = name_box[1] + (name_box[3] - name_box[1] - font_height) / 2
        draw.text((new_width, new_height), text, fill="black", font=name_font)

        COSTS_BOX = (0.25, 0.55, 1.0, 0.65)
        costs_box = self.percent_tuple_to_px(COSTS_BOX, True, False)
        draw.rectangle(costs_box,fill="white",outline ="black")

        # Draw costs symbols
        card_dungeon_stats = self.card.stats
        stats_text = card_dungeon_stats.stats_to_string()
        emote_text_box = centered_text_position_in_box(emote_font, stats_text, costs_box)
        with Pilmoji(card_image) as pilmoji:
            pilmoji.text(emote_text_box, stats_text, (0, 0, 0), emote_font)

        DESCRIPTION_BOX = (0.1, 0.65, 1.00, 0.9)
        description_box = self.percent_tuple_to_px(DESCRIPTION_BOX, True, False)
        draw.rectangle(description_box,fill=None,outline ="red")

        # Card Description text:
        (x1,y1,x2,y2) = description_box
        description_box_wh = (x1, y1, x2-x1, y2-y1)
        emoji_text_box(self.card.text, card_image, description_font, description_box_wh, fill="black")
        # with Pilmoji(card_image) as pilmoji:
        #    pilmoji.text((int(description_box[0]), int(description_box[1])), self.card.text, (0, 0, 0), description_font)

        return card_image

class PDFGridBuilder:
    def __init__(self, cards, grid_size=(3, 3), card_size_cm=(6.3, 8.8), margin_cm=0.5):
        # Convert card and margin sizes from cm to pixels
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.margin_px = cm_to_px(margin_cm)

        self.cards = cards
        self.grid_size = grid_size  # 3x3 grid

        # Calculate the size of the full sheet in pixels
        self.sheet_size = (
            (self.card_size_px[0] + self.margin_px) * self.grid_size[0] - self.margin_px,
            (self.card_size_px[1] + self.margin_px) * self.grid_size[1] - self.margin_px
        )

    def build_grid(self, cards_subset):
        # Create a blank sheet to hold the grid
        sheet = Image.new('RGB', self.sheet_size, color=(255, 255, 255))

        # Paste each card onto the grid
        for i, card_image in enumerate(cards_subset):
            x_offset = (self.card_size_px[0] + self.margin_px) * (i % self.grid_size[0])
            y_offset = (self.card_size_px[1] + self.margin_px) * (i // self.grid_size[0])
            sheet.paste(card_image, (x_offset, y_offset))

        return sheet

    def save_as_pdf(self, output_pdf_path):
        # Divide cards into chunks based on the grid size
        max_cards_per_page = self.grid_size[0] * self.grid_size[1]
        card_chunks = [self.cards[i:i + max_cards_per_page] for i in range(0, len(self.cards), max_cards_per_page)]

        # Initialize the PDF object
        pdf = FPDF(orientation='P', unit='pt', format=(cm_to_px(21), cm_to_px(29.7)))  # A4 size in pixels

        for number,chunk in enumerate(card_chunks):
            # Build the grid for the current chunk of cards
            grid_image = self.build_grid(chunk)

            # Convert the PIL image to a temporary file to use with FPDF
            grid_image_path = f'tmp/grid_image{str(number)}.png'
            grid_image.save(grid_image_path)

            # Add a new page to the PDF and insert the image
            pdf.add_page()
            pdf.image(grid_image_path, 0, 0, w=cm_to_px(21), h=cm_to_px(29.7))  # Adjust to A4 size

        # Output the PDF to a file
        pdf.output(output_pdf_path)
