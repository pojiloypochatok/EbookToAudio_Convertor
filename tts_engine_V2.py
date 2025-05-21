import os
import torch
from pydub import AudioSegment
import asyncio

# Загрузка модели
language = 'ru'
model_id = 'v4_ru'
device = torch.device('cpu')
output_path = "output.wav"
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
def generate_ssml(text, pitch="low", rate="slow", strength="strong", volume=None):
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
def synthesize_and_merge(text):
    chunks = split_text_by_length(text)
    temp_files = []

    for idx, chunk in enumerate(chunks):
        temp_path = f"chunk_{idx}.wav"
        model.save_wav(text=chunk,
                       speaker=speaker,
                       sample_rate=sample_rate,
                       audio_path=temp_path)
        temp_files.append(temp_path)

    final_audio = AudioSegment.empty()
    for path in temp_files:
        final_audio += AudioSegment.from_wav(path)

    return final_audio

    for path in temp_files:
        os.remove(path)


def generate_text(text):
    return synthesize_and_merge(text)


book = """
    Они работали без устали, до седьмого пота, только бы убрать сено! Труды их не пропали даром, урожай выдался на славу, они и не надеялись собрать такой.
    Порой они отчаивались, потому что коса, грабли — они ведь не для животных, для людей приспособлены: ни одному животному с ними не управиться, тут требуется стоять на задних ногах. Но свиньи — вот ведь умные! — из любого положения находили выход. Ну а лошади, те знали поле досконально, а уж косили и сгребали в валки так, как и не свилось Джонсу и его работникам. Сами свиньи в поле не работали, они взяли на себя общее руководство и надзор. Да иначе и быть не могло, при их-то учёности. Боец и Кашка впрягались в косилку, а то и в конные грабли (им, конечно, не требовалось ни удил, ни уздечек) и упорно ходили круг за кругом по полю, а кто-нибудь из свиней шел сзади и покрикивал когда «А ну, товарищ, наддай!», а когда «А ну, товарищ, осади назад!». А уж ворошили и копнили сено буквально все животные от мала до велика. Утки и куры и те весь день носились взад-вперед, по клочкам перетаскивая сено в клювах. Завершили уборку досрочно. Джонс с работниками наверняка провозился бы по меньшей мере еще два дня. Не говоря уж о том, что такого урожая на ферме сроду не видывали, вдобавок убрали его без потерь: куры и утки — они же зоркие — унесли с поля все до последней былинки. И никто ни клочка не украл.
"""

result = generate_text(book)
result.export("output.wav", format="wav")


