# EbookToAudio Convertor (Silero TTS V5)

Конвертер текста в аудио на базе Silero TTS V5 с CLI, поддержкой глав, прогресса и гибкой настройки голоса.

## Возможности
- Разбиение текста на главы (детектор по заголовкам) или на предложения с интеллектуальной упаковкой в чанки.
- Поддержка Silero TTS V5 (русский), кэш модели в `~/.ebooktoaudio/models/v5_ru.pt`.
- Настройка диктора, скорости, высоты, длины чанков через CLI.
- Отложенное выполнение в отдельном потоке с отслеживанием прогресса.

## Требования
- Python 3.10+
- torch, pydub, scipy, audioop-lts (см. `requirements.txt`)
- FFmpeg установлен в системе (для pydub).

## Установка
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск (CLI)
```bash
python run_cli.py --file input/book.txt --output-name Book
```
Опции:
- `--text "Привет"` — текст напрямую.
- `--speaker eugene|baya|kseniya|xenia|aidar` — выбор диктора.
- `--rate x-slow|slow|medium|fast|x-fast` — скорость речи.
- `--pitch x-low|low|medium|high|x-high` — высота.
- `--chunk-len 400` — размер чанка (символы) при синтезе.

Пример с настройкой:
```bash
python run_cli.py --file input/book.txt --output-name Book --speaker kseniya --rate slow --pitch low --chunk-len 450
```

Результат сохраняется в `output/<name>.wav`. При первом запуске модель скачивается в `~/.ebooktoaudio/models/`.

## Структура
- `EbookToAudio_Engine/ebooktoaudio_manager.py` — основной сервис, логика прогресса и ветвление по главам.
- `EbookToAudio_Engine/utils/V2/tts_engine_V2.py` — загрузка модели, разбиение текста, синтез и склейка.
- `run_cli.py` — консольный интерфейс.
- `input/`, `output/`, `temp/` — входные, выходные и временные файлы.

## Программное использование
```python
from EbookToAudio_Convertor import EbookToAudio

svc = EbookToAudio()
svc.auto_generate(r"input/book.txt", filename="Book", task_id="job1")
# прогресс: svc.get_progress("job1")
```

## Зависимости модели
По умолчанию используется русский V5 (`v5_ru.pt`) с Silero Models: https://github.com/snakers4/silero-models

## Замечания
- Длинные предложения автоматически режутся по символам, если превышают лимит чанка.
- Для корректной работы pydub нужен FFmpeg в PATH.

