from PIL import Image, ImageDraw, ImageFont

# Constants
DPI = 300  # Dots per inch
CM_TO_INCH = 2.54

# Convert centimeters to pixels at 300 DPI
def cm_to_px(cm, dpi=DPI):
    return int((cm / CM_TO_INCH) * dpi)

class CardBuilder:
    def __init__(self, card_data, card_size_cm=(6.3, 8.8)):
        # Convert card size from cm to pixels
        self.card_size_px = (cm_to_px(card_size_cm[0]), cm_to_px(card_size_cm[1]))
        self.card_data = card_data
        self.card_template = 'src/2167149428_8f9a5c242e_b.jpg'  # A base card template image

    def build_card(self):
        # Open a card template or create a blank card
        card_image = Image.open(self.card_template).resize(self.card_size_px)  # Resize template to match card size
        draw = ImageDraw.Draw(card_image)

        # Font setup (customize this with your own font)
        try:
            font = ImageFont.truetype("assets/font.ttf", 20)
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if TTF is missing

        # Draw text (name, attack, defense, description)
        draw.text((20, 20), self.card_data['name'], font=font, fill=(0, 0, 0))
        draw.text((20, 60), f"Attack: {self.card_data['attack']}", font=font, fill=(0, 0, 0))
        draw.text((20, 100), f"Defense: {self.card_data['defense']}", font=font, fill=(0, 0, 0))
        draw.text((20, 140), self.card_data['description'], font=font, fill=(0, 0, 0))

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

    def build_grid(self):
        # Create a blank sheet to hold the grid
        sheet = Image.new('RGB', self.sheet_size, color=(255, 255, 255))

        # Paste each card onto the grid
        for i, card_image in enumerate(self.cards):
            x_offset = (self.card_size_px[0] + self.margin_px) * (i % self.grid_size[0])
            y_offset = (self.card_size_px[1] + self.margin_px) * (i // self.grid_size[0])
            sheet.paste(card_image, (x_offset, y_offset))

        return sheet

# Generate some hardcoded card data
def generate_sample_cards():
    sample_cards = [
        {"name": "Card 1", "attack": "100", "defense": "200", "description": "A powerful card."},
        {"name": "Card 2", "attack": "150", "defense": "100", "description": "A fast card."},
        {"name": "Card 3", "attack": "120", "defense": "220", "description": "A balanced card."},
        {"name": "Card 4", "attack": "200", "defense": "150", "description": "A strong card."},
        {"name": "Card 5", "attack": "130", "defense": "140", "description": "An agile card."},
        {"name": "Card 6", "attack": "170", "defense": "190", "description": "A powerful card."},
        {"name": "Card 7", "attack": "110", "defense": "100", "description": "A weak card."},
        {"name": "Card 8", "attack": "160", "defense": "180", "description": "A resilient card."},
        {"name": "Card 9", "attack": "140", "defense": "170", "description": "A defensive card."},
    ]
    return sample_cards

# Main execution
if __name__ == '__main__':
    # Build the sample cards
    card_data_list = generate_sample_cards()
    cards = []
    for card_data in card_data_list:
        builder = CardBuilder(card_data)
        card_image = builder.build_card()
        cards.append(card_image)

    # Build the grid and save it as a PDF
    grid_builder = PDFGridBuilder(cards)
    grid_image = grid_builder.build_grid()

    # Save as PDF with the correct DPI for printing
    grid_image.save("output/cards_grid.pdf", "PDF", resolution=DPI)
