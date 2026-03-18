import genanki
import random
from pathlib import Path


class CardManager:
    """
    Manages creation of Anki cards and deck export-
    Uses a simple Basic card which Front contains
    image + sentence + audio and Back an user input.
    """

    def __init__(self):

        self.model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            "Basic Media Card",

            fields=[
                {"name": "Front"},
                {"name": "Back"},
            ],

            templates=[
                {
                    "name": "Card 1",

                    "qfmt": """
                    {{Front}}
                    """,

                    "afmt": """
                    {{Front}}
                    <hr>
                    {{Back}}
                    """
                }
            ],

            css="""
            .card {
                font-family: Arial;
                font-size: 26px;
                text-align: center;
                color: black;
                background-color: white;
            }

            img {
                max-width: 400px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            """
        )

        self.deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
            "Media Audio Deck"
        )

        self.media_files = []

    

    def add_card(self, sentence, translation, audio_file, image_file=None):

        front = sentence

        if image_file:
            img_name = Path(image_file).name
            front += f'<br><img src="{img_name}">'
            self.media_files.append(image_file)

        audio_name = Path(audio_file).name
        front += f"<br>[sound:{audio_name}]"

        self.media_files.append(audio_file)

        note = genanki.Note(
            model=self.model,
            fields=[
                front,
                translation
            ]
        )

        self.deck.add_note(note)

    
    def export(self, output_path):

        package = genanki.Package(self.deck)
        package.media_files = self.media_files
        package.write_to_file(output_path)
        package.write_to_file(output_path)