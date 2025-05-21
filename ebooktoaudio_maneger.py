from .extract_characters import split_into_chapters
from .tts_engine_V2 import generate_text

class BookManager():
    def __init__(self):
        self.temp_path = "",
        self.output_path = "",

    def generate_with_characters(self, unsplit_text):
        characters = split_into_chapters(unsplit_text)
        for character in characters:
            generate_text(character)

