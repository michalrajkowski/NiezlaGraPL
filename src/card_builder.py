from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from card import Card
from fpdf import FPDF

# Constants
DPI = 300  # Dots per inch
CM_TO_INCH = 2.54
SYMBOLA_FONT_PATH = "/home/noodles/.fonts/Symbola.ttf"

# Convert centimeters to pixels at 300 DPI
def cm_to_px(cm, dpi=DPI):
    return int((cm / CM_TO_INCH) * dpi)

class CardBuilder:
    def __init__(self, card : Card, card_size_cm=(6.3, 8.8)):
        # Convert card size from cm to pixels
        self.card_size_cm = card_size_cm
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.card = card

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
