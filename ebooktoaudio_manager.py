from torch.cuda.tunable import read_file

from utils.V2.extract_characters import split_into_chapters
from utils.V2.tts_engine_V2 import generate_text
import os
import typing


class BookManager():
    def __init__(self, temp_path, output_path, input_path):
        self.temp_path = temp_path,
        self.output_path = output_path,
        self.input_path = input_path

    def read_file(self, input_file):
        #В будущем здесь планирурется конвертация всех форматов
        file_name = __name__(input_file)
        with open(input_file) as file:
            return file, file_name

    def generate_with_characters(self, unsplit_text):
        if unsplit_text is not str:
            unsplit_text, file_name = read_file(unsplit_text)
            print(unsplit_text, file_name)
        characters = split_into_chapters(unsplit_text)
        for idx, character in enumerate(characters):
            generate_text(character, f"{self.output_path}/{file_name}(character{idx})", self.temp_path)

    def generate_without_characters(self, input_text):
        if input_text is not str:
            input_text, file_name = read_file(input_text)
            print(input_text, file_name)
        generate_text(input_text, f"{self.output_path}/{file_name}", self.temp_path)

ebooktoaudio = BookManager(output_path=r"output", temp_path=r"temp", input_path="input")