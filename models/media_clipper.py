import ffmpeg
from pathlib import Path


class MediaClipper:
    """
    Extracts audio segments from media files that are supported.
    """

    def __init__(self, media_path: str):

        self.media_path = media_path
        Path("audio").mkdir(exist_ok=True)

    def extract_audio(self, start: float, end: float, clip_number: int) -> str:

        output = f"audio/clip_{clip_number}.mp3"

        (
            ffmpeg
            .input(self.media_path, ss=start, to=end)
            .output(output, acodec="mp3", vn=None)
            .run(overwrite_output=True)
        )

        return output