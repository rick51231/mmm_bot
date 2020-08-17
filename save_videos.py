from pytube import YouTube, StreamQuery
import traceback

from core.settings import BASE_DIR

StreamQuery

SAVE_PATH = f"{BASE_DIR}/video"

link = [
    # "https://www.youtube.com/watch?v=u4Q0KIcxt4Q",  "https://www.youtube.com/embed/2oIITQ_X930"
    #   "https://www.youtube.com/watch?v=6aih26QnF0c",  "https://www.youtube.com/embed/HlTsC-Qmsbk"
    #  "https://www.youtube.com/watch?v=Sr-AJ-8gZbU&feature=share", "https://www.youtube.com/embed/aB2rEoh87f0",
    #   "https://www.youtube.com/watch?v=AWwF24jQCQE" "https://www.youtube.com/embed/AYjKDmWPLTs"
    # "youtube.com/embed/2Ku0DgNLcGc",
    # "youtube.com/embed/v_oXt6vBbyU",
    # "youtube.com/embed/EhB__Cmmc-w",
    # "https://www.youtube.com/watch?v=VVHIDJGG7dE&feature=emb_logo"

]
for i in link:
    try:
        yt = YouTube(i)
    except:
        traceback.print_exc()
        continue

    stream = yt.streams.get_highest_resolution()

    try:
        print(f"Скачиваем {yt.title}")
        stream.download(filename=yt.title, output_path=SAVE_PATH)
    except:
        traceback.print_exc()
        continue
print('Task Completed!')
