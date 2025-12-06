import os
import re
from pathlib import Path

import torch
from pydub import AudioSegment

from .progress_tracker import ProgressTracker

MODEL_URL = "https://models.silero.ai/models/tts/ru/v5_ru.pt"
MODEL_DIR = Path.home() / ".ebooktoaudio" / "models"
MODEL_LOCAL_PATH = MODEL_DIR / "v5_ru.pt"
DEVICE = torch.device("cpu")
SAMPLE_RATE = 48000
SPEAKER = "eugene"
DEFAULT_PITCH = "low"
DEFAULT_RATE = "slow"
CHUNK_LEN = 400


def _ensure_model():
    if not MODEL_LOCAL_PATH.exists():
        MODEL_LOCAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        torch.hub.download_url_to_file(MODEL_URL, MODEL_LOCAL_PATH)

    model_instance = torch.package.PackageImporter(MODEL_LOCAL_PATH).load_pickle(
        "tts_models", "model"
    )
    model_instance.to(DEVICE)
    return model_instance


model = _ensure_model()


def generate_ssml(text, pitch=DEFAULT_PITCH, rate=DEFAULT_RATE, volume=None):
    prosody_attrs = f'pitch="{pitch}" rate="{rate}"'
    if volume:
        prosody_attrs += f' volume="{volume}"'

    return f'<speak><prosody {prosody_attrs}>{text}</prosody></speak>'


def split_text_by_length(text, max_len=None):
    max_len = max_len or CHUNK_LEN
    sentences = re.split(r"(?<=[\.!\?\…])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s and s.strip()]

    chunks = []
    buf = []
    buf_len = 0

    for sent in sentences:
        if len(sent) > max_len:
            for i in range(0, len(sent), max_len):
                part = sent[i : i + max_len].strip()
                if part:
                    chunks.append(generate_ssml(part))
            continue

        if buf_len + len(sent) + 1 <= max_len:
            buf.append(sent)
            buf_len += len(sent) + 1
        else:
            if buf:
                merged = " ".join(buf).strip()
                if merged:
                    chunks.append(generate_ssml(merged))
            buf = [sent]
            buf_len = len(sent)

    if buf:
        merged = " ".join(buf).strip()
        if merged:
            chunks.append(generate_ssml(merged))

    return chunks


def synthesize_and_merge(text, absol_temp_path, on_progress=None):
    chunks = split_text_by_length(text, CHUNK_LEN)
    if not chunks:
        raise ValueError("Передан пустой текст для синтеза")

    os.makedirs(absol_temp_path, exist_ok=True)
    progress_idx = round(100 / len(chunks))
    temp_files = []

    for idx, chunk in enumerate(chunks):
        temp_path = f"{absol_temp_path}/chunk_{idx}.wav"
        model.save_wav(
            ssml_text=chunk,
            speaker=SPEAKER,
            sample_rate=SAMPLE_RATE,
            audio_path=temp_path,
        )
        temp_files.append(temp_path)
        if on_progress:
            on_progress(progress_idx)

    final_audio = AudioSegment.empty()
    for path in temp_files:
        final_audio += AudioSegment.from_wav(path)

    for path in temp_files:
        os.remove(path)

    return final_audio


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


def set_config(speaker=None, pitch=None, rate=None, sample_rate=None, chunk_len=None):
    global SPEAKER, DEFAULT_PITCH, DEFAULT_RATE, SAMPLE_RATE, CHUNK_LEN
    if speaker:
        SPEAKER = speaker
    if pitch:
        DEFAULT_PITCH = pitch
    if rate:
        DEFAULT_RATE = rate
    if sample_rate:
        SAMPLE_RATE = sample_rate
    if chunk_len:
        CHUNK_LEN = max(1, int(chunk_len))




