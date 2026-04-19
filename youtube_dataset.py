from pytube import YouTube
import os

# -------------------------
# ACTIVITY LINKS (ADD YOUR OWN)
# -------------------------

video_links = {
    "walking": [
        "https://www.youtube.com/watch?v=XXXX1",
        "https://www.youtube.com/watch?v=XXXX2",
        "https://www.youtube.com/watch?v=XXXX3"
    ],
    "sitting": [
        "https://www.youtube.com/watch?v=XXXX4",
        "https://www.youtube.com/watch?v=XXXX5",
        "https://www.youtube.com/watch?v=XXXX6"
    ],
    "dancing": [
        "https://www.youtube.com/watch?v=XXXX7",
        "https://www.youtube.com/watch?v=XXXX8",
        "https://www.youtube.com/watch?v=XXXX9"
    ],
    "jumping": [
        "https://www.youtube.com/watch?v=XXXX10",
        "https://www.youtube.com/watch?v=XXXX11",
        "https://www.youtube.com/watch?v=XXXX12"
    ],
    "running": [
        "https://www.youtube.com/watch?v=XXXX13",
        "https://www.youtube.com/watch?v=XXXX14",
        "https://www.youtube.com/watch?v=XXXX15"
    ],
    "drinking": [
        "https://www.youtube.com/watch?v=XXXX16",
        "https://www.youtube.com/watch?v=XXXX17",
        "https://www.youtube.com/watch?v=XXXX18"
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
                yt = YouTube(link)
                stream = yt.streams.filter(file_extension='mp4', progressive=True).first()

                filename = f"{activity}_{i}.mp4"
                stream.download(output_path=save_path, filename=filename)

                print(f"✔ Downloaded: {filename}")

            except Exception as e:
                print(f"❌ Failed: {link}")
                print("Error:", e)

    print("\nALL DOWNLOADS COMPLETE!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    download_videos()