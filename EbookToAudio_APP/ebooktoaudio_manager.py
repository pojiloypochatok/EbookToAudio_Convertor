import os
import threading
from pathlib import Path
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.extract_characters import split_into_chapters
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.check_for_characters import check_characters
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.tts_engine_V2 import generate_text
from EbookToAudio_Convertor.EbookToAudio_APP.utils.V2.progress_tracker import ProgressTracker


def read_file(input_file):
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
        self.active_trackers = {}  # task_id -> ProgressTracker

    def _track(self, task_id):
        tracker = ProgressTracker()
        self.active_trackers[task_id] = tracker
        return tracker

    def get_progress(self, task_id="default"):
        tracker = self.active_trackers.get(task_id)
        if tracker:
            return tracker

        return {"error": "Invalid task ID"}

    def generate_with_characters(self, unsplit_text, file_name, tracker: ProgressTracker):
        characters = split_into_chapters(unsplit_text)
        total = len(characters)

        for idx, character in enumerate(characters):
            generate_text(
                character,
                f"{self.output_path}/{file_name}(character{idx}).wav",
                self.temp_path,
                progress_tracker=tracker,
                base_progress=int((idx / total) * 100),
                part_ratio=int(100 / total)
            )

        tracker.mark_done()

    def generate_without_characters(self, input_text, file_name, tracker: ProgressTracker):
        generate_text(
            input_text,
            f"{self.output_path}/{file_name}.wav",
            self.temp_path,
            progress_tracker=tracker
        )
        tracker.mark_done()

    def auto_generate(self, input_text, filename="Untitled", task_id="default"):
        if not isinstance(input_text, str) and os.path.isfile(input_text):
            input_text, filename = read_file(input_text)

        tracker = self._track(task_id)

        def task():
            try:
                if check_characters(input_text):
                    self.generate_with_characters(input_text, filename, tracker)
                else:
                    self.generate_without_characters(input_text, filename, tracker)
            except Exception as e:
                tracker.set_error(e)

        threading.Thread(target=task).start()
