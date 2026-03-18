import pysrt

class SubtitleManager:
    """
    Loads and manages subtitles from an SRT file.
    """

    def __init__(self, srt_path: str):

        self.subs = pysrt.open(srt_path)

    def get_all(self):

        data = []

        for sub in self.subs:

            start = sub.start.ordinal / 1000
            end = sub.end.ordinal / 1000

            data.append({
                "start": start,
                "end": end,
                "text": sub.text
            })

        return data