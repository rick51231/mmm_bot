from pytube import YouTube
import traceback

from core.settings import BASE_DIR

SAVE_PATH = f"{BASE_DIR}/video"

link = ["https://www.youtube.com/embed/uhMQmdtp6Ro",
        "https://www.youtube.com/embed/rIsdgr0BTzY",
        "https://www.youtube.com/embed/YwqiuggLFoQ",
        "https://www.youtube.com/embed/Dx8i8W0uVYA",
        "https://www.youtube.com/embed/2Ku0DgNLcGc",
        "https://www.youtube.com/embed/v_oXt6vBbyU",
        "https://www.youtube.com/embed/EhB__Cmmc-w",

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
