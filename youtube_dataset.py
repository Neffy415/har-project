import os
from yt_dlp import YoutubeDL


class _QuietLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

# -------------------------
# ACTIVITY LINKS (ADD YOUR OWN)
# -------------------------

video_links = {
    "walking": [
        "https://youtu.be/GBkJY86tZRE?si=nB634XX5SaXP0Kv_",
        "https://youtu.be/F-Xy3_ln_BY?si=w4SivkM2ZtalQ-Nv",
        "https://youtube.com/shorts/tH3FfSfefJw?si=oiPsvoB1xcjVUrZi"
    ],
    "resting": [
        "https://youtube.com/shorts/Zf7Iyqa7jp8?si=ESaGz3Uu2tULtUg-",
        "https://youtube.com/shorts/XSePplGXdSM?si=8No3m_uR5inODFdH",
        "https://youtube.com/shorts/aimCKWTZlWo?si=_-K5kIwzEwZRv9WZ"
    ],
    "talking": [
        "https://youtube.com/shorts/Q2cumSDBFUY?si=C-65IPBVgRt3OGpD",
        "https://youtube.com/shorts/-3VY3tqzFaQ?si=Mel47LTzBqkIlvfr",
        "https://youtube.com/shorts/tjSznYrIGVI?si=c6hV-OTZiz5_R4Fy"
    ],
    "standing": [
        "https://youtube.com/shorts/uq-dnH51Lko?si=WqZbeJsK6zoWQ2J8",
        "https://youtube.com/shorts/97_oHyGMVGA?si=LAvyZjX2_p1Ys7md",
        "https://youtube.com/shorts/i0WCgfZZ0Vo?si=kRze2v9knIBkbm0R"
    ]
}

# -------------------------
# DOWNLOAD FUNCTION
# -------------------------
def download_videos():
    base_dir = "dataset"
    os.makedirs(base_dir, exist_ok=True)

    for activity, links in video_links.items():
        save_path = os.path.join(base_dir, activity)
        os.makedirs(save_path, exist_ok=True)

        print(f"\nDownloading: {activity}")

        for i, link in enumerate(links):
            try:
                filename_template = os.path.join(save_path, f"{activity}_{i}.%(ext)s")
                ydl_opts = {
                    "format": "mp4/best[ext=mp4]/best",
                    "outtmpl": filename_template,
                    "quiet": True,
                    "no_warnings": True,
                    "noplaylist": True,
                    "merge_output_format": "mp4",
                    "windowsfilenames": True,
                    "logger": _QuietLogger(),
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                print(f"Downloaded: {activity}_{i}.mp4")

            except Exception as e:
                print(f"Failed: {link}")
                print("Error:", e)

    print("\nAll downloads complete!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    download_videos()