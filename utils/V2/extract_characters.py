import re
from pydub import AudioSegment

def split_into_chapters(text):
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
        return [("Весь текст", text.strip())]

    chapters = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = match.group(0).strip()
        content = text[start:end].strip()
        chapters.append((title, content))

    print(chapters)
    return chapters
