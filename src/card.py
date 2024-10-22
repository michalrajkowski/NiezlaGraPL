class Card:
    def __init__(self, name, art, text):
        self.name = name
        self.art = art
        self.text = text

    @classmethod
    def from_defaults(cls):
        return cls(name="Default Name", art="Default Art", text="Default Text")
    
    @classmethod
    def blank_card(cls):
        return cls(name="", art="", text="")

    def __repr__(self):
        return f"<Card(name={self.name}, attack={self.art}, defense={self.text})>"
