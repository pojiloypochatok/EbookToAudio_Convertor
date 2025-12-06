import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_PARENT = ROOT.parent

for candidate in (ROOT, PROJECT_PARENT):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from EbookToAudio_Convertor import EbookToAudio  # type: ignore
from EbookToAudio_Convertor.EbookToAudio_Engine.utils.V2 import tts_engine_V2 as tts  # type: ignore


def parse_args():
    parser = argparse.ArgumentParser(
        description="Консольный запуск конвертации текста/файла в аудио через Silero TTS V5."
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Текст для озвучки.")
    src.add_argument("--file", help="Путь к текстовому файлу для озвучки.")

    parser.add_argument(
        "--output-name",
        default="Untitled",
        help="Имя выходного файла (без расширения). По умолчанию Untitled.",
    )
    parser.add_argument(
        "--task-id",
        default="default",
        help="ID задачи для отслеживания прогресса (если запускаете несколько).",
    )
    parser.add_argument("--speaker", help="Имя диктора (например, eugene, baya, kseniya).")
    parser.add_argument(
        "--rate",
        choices=["x-slow", "slow", "medium", "fast", "x-fast"],
        help="Скорость речи.",
    )
    parser.add_argument(
        "--pitch",
        choices=["x-low", "low", "medium", "high", "x-high"],
        help="Высота голоса.",
    )
    parser.add_argument(
        "--chunk-len",
        type=int,
        help="Максимальная длина чанка (символы) перед синтезом.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.file and not os.path.isfile(args.file):
        print(f"Файл не найден: {args.file}")
        sys.exit(1)

    tts.set_config(
        speaker=args.speaker,
        pitch=args.pitch,
        rate=args.rate,
        chunk_len=args.chunk_len,
    )

    svc = EbookToAudio()
    src_value = args.text if args.text is not None else args.file

    svc.auto_generate(src_value, filename=args.output_name, task_id=args.task_id)
    print("Генерация запущена, подождите...")

    # Простейший опрос прогресса
    while True:
        tracker = svc.get_progress(args.task_id)
        if isinstance(tracker, dict) and "error" in tracker:
            print(f"Ошибка: {tracker['error']}")
            sys.exit(1)

        err = tracker.get_error()
        if err:
            print(f"Ошибка: {err}")
            sys.exit(1)

        progress = tracker.get()
        print(f"\rПрогресс: {progress:3d}%", end="", flush=True)

        if tracker.is_done():
            print("\nГотово! Файл(ы) лежат в папке output.")
            break

        time.sleep(0.5)


if __name__ == "__main__":
    main()

