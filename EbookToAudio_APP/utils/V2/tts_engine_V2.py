import os
import torch
from pydub import AudioSegment
from .progress_tracker import ProgressTracker

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
    ssml = f'<speak><prosody {prosody_attrs}>{text}</prosody></speak>'
    return ssml


# Деление текста на части
def split_text_by_length(text, max_len=800):
    chunks = [text[i:i + max_len] for i in range(0, len(text), max_len)]
    for chunk in chunks:
        chunk = generate_ssml(chunk)
    return chunks


# Озвучка и склейка
def synthesize_and_merge(text, absol_temp_path, on_progress=None):
    chunks = split_text_by_length(text)
    progress_idx = round(100 / len(chunks))
    print(progress_idx)
    temp_files = []

    for idx, chunk in enumerate(chunks):
        temp_path = f"{absol_temp_path}/chunk_{idx}.wav"
        model.save_wav(text=chunk,
                       speaker=speaker,
                       sample_rate=sample_rate,
                       audio_path=temp_path)
        temp_files.append(temp_path)
        if on_progress:
            on_progress(progress_idx)

    final_audio = AudioSegment.empty()
    for path in temp_files:
        final_audio += AudioSegment.from_wav(path)

    for path in temp_files:
        os.remove(path)

    return final_audio


# Основная функция
def generate_text(text, output_path, temp_path, progress_tracker: ProgressTracker = None):
    try:
        def on_progress(local_percent):
            if progress_tracker:
                global_percent = progress_tracker.get()
                global_percent += local_percent
                progress_tracker.set(global_percent)

        result = synthesize_and_merge(text, temp_path, on_progress=on_progress)
        result.export(output_path, format="wav")
        if progress_tracker:
            progress_tracker.mark_done()

    except Exception as e:
        if progress_tracker:
            progress_tracker.set_error(e)
        raise

    finally:
        print(f"Аудиофайл успешно сгенерирован и находится в {output_path}")




