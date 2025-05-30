import re
from pydub import AudioSegment

def check_characters(text):
    chapter_patterns = [
        r'^\s*(Глава\s+\d+)\s*$',
        r'^\s*(Глава\s+[IVXLCDM\d]+)\s*$',
        r'^\s*(Часть\s+[IVXLCDM]+)\s*$',     # Римские цифры
        r'^\s*(Часть\s+\d+)\s*$',             # Арабские цифры
        r'^\s*(CHAPTER\s+[IVXLCDM]\d]+)\s*$',  # CHAPTER I / 1
        r'^\s*(\d{1,2})\s*$',                 # Просто число
    ]

    combined_pattern = re.compile('|'.join(chapter_patterns), re.MULTILINE | re.IGNORECASE)

    matches = list(combined_pattern.finditer(text))

    if not matches:
        return False

    else:
        return True
