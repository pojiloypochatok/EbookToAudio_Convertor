from torch.cuda.tunable import read_file  # если используешь read_file из torch
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.extract_characters import split_into_chapters
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.tts_engine_V2 import generate_text
import os
from pathlib import Path


def read_file(input_file):
    # В будущем здесь планируется конвертация всех форматов
    filename = os.path.splitext(os.path.basename(input_file))[0]
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
        return content, filename


class EbookToAudio:
    def __init__(self, output_path: str = "output", input_path: str = "input"):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.temp_path = self.BASE_DIR / "temp"
        self.output_path = self.BASE_DIR / output_path
        self.input_path = self.BASE_DIR / input_path

    def generate_with_characters(self, unsplit_text):
        if unsplit_text is not str:
            unsplit_text, file_name = read_file(unsplit_text)
            print(unsplit_text, file_name)

        characters = split_into_chapters(unsplit_text)
        for idx, character in enumerate(characters):
            generate_text(
                character,
                f"{self.output_path}/{file_name}(character{idx})",
                self.temp_path
            )

    def generate_without_characters(self, input_text):
        if not isinstance(input_text, str):
            input_text, file_name = read_file(input_text)
            print(input_text, file_name)
        else:
            file_name = "untitled"
        generate_text(
            input_text,
            f"{self.output_path}/{file_name}.wav",
            self.temp_path
        )

