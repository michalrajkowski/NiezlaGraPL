from card import CardColor
COLOR_TO_EMOJI = {
    CardColor.NONE: "⚪",   # White circle for NONE
    CardColor.RED: "🔴",   # Red circle
    CardColor.GREEN: "🟢",  # Green circle
    CardColor.BLUE: "🔵",   # Blue circle
    CardColor.YELLOW: "🟡", # Yellow circle
    CardColor.PURPLE: "🟣", # Purple circle
}

# Method to get the emoji
def color_to_emoji(color: CardColor) -> str:
    return COLOR_TO_EMOJI.get(color, "")

def multi_cost_to_emoji_text(cost) -> str:
    emoji_text = ""
    for color, amount in cost.items():
        if amount > 0:
            emoji_text += color_to_emoji(color) * amount
    return emoji_text