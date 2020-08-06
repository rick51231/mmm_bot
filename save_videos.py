from pytube import YouTube
import traceback

from core.settings import BASE_DIR

Stream

SAVE_PATH = f"{BASE_DIR}/video"

link = ["youtube.com/embed/uhMQmdtp6Ro",
        "youtube.com/embed/rIsdgr0BTzY",
        "youtube.com/embed/YwqiuggLFoQ",
        "youtube.com/embed/Dx8i8W0uVYA",
        "youtube.com/embed/2Ku0DgNLcGc",
        "youtube.com/embed/v_oXt6vBbyU",
        "youtube.com/embed/EhB__Cmmc-w",

        ]
for i in link:
    try:
        yt = YouTube(i)
    except:
        traceback.print_exc()
        continue

    stream = yt.streams.first()

    try:
        stream.download(filename=yt.title, output_path=SAVE_PATH)
    except:
        traceback.print_exc()
        continue
print('Task Completed!')
