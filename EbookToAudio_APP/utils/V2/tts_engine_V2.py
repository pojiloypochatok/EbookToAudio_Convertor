import os
import torch
from pydub import AudioSegment
import asyncio

# Загрузка модели
language = 'ru'
model_id = 'v4_ru'
device = torch.device('cpu')
sample_rate = 48000
speaker = "eugene"

model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language=language,
    speaker=model_id
)
model.to(device)


# Создание ssml из текста
def generate_ssml(text, pitch="low", rate="very-slow", strength="strong", volume=None):
    prosody_attrs = f'pitch="{pitch}" rate="{rate}" strength="{strength}"'
    if volume:
        prosody_attrs += f' volume="{volume}"'

    ssml = f'<speak><prosody {prosody_attrs}>{text}</prosody></speak>'
    return ssml


# Деление текста на части
def split_text_by_length(text, max_len=800):
    chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        chunk = generate_ssml(chunk)
    return chunks


# Озвучка + склейка
def synthesize_and_merge(text, absol_temp_path):
    chunks = split_text_by_length(text)
    temp_files = []

    for idx, chunk in enumerate(chunks):
        temp_path = f"{absol_temp_path}/chunk_{idx}.wav"
        model.save_wav(text=chunk,
                       speaker=speaker,
                       sample_rate=sample_rate,
                       audio_path=temp_path)
        temp_files.append(temp_path)

    final_audio = AudioSegment.empty()
    for path in temp_files:
        final_audio += AudioSegment.from_wav(path)

    for path in temp_files:
        os.remove(path)

    return final_audio


def generate_text(text, output_path, temp_path):
    try:
        result = synthesize_and_merge(text, temp_path)
        result.export(output_path, format="wav")
    finally:
        print(f"Аудиофайл успешно сгенерирован и находится в {output_path}")



