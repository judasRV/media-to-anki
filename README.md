# Media to Anki

A simple desktop tool to create Anki cards with audio (and optional images) from video/audio files and subtitles.

<img width="1136" height="541" alt="example" src="https://github.com/user-attachments/assets/669be7b9-d767-40b5-a990-e73580b456be" />

## Features

* Extract audio clips from video or audio files
* Load `.srt` subtitles
* Search inside subtitles
* Auto-fill start/end times from subtitles
* Create cards with:

  * sentence
  * translation
  * audio
  * optional image
* Export directly to Anki (`.apkg`)

## Usage

1. Open a video or audio file
2. (Optional) Load an `.srt` subtitle file
3. Search or select a subtitle
4. Adjust start/end times if needed
5. Add optional image
6. Create card
7. Export deck

## Requirements

* Python 3.x
* ffmpeg installed or included

Install dependencies:

genanki
ffmpeg-python*
pysrt

## Build executable

Using PyInstaller:

```
pyinstaller --onefile --noconsole main.py
```

## Output

Exports an `.apkg` file ready to import into Anki.

## Notes

* Audio is embedded in the deck
* Image is optional per card

## Future improvements

* Card preview/edit window
* Duplicate detection
* Batch generation from subtitles
* Tagging per source file

## License

MIT
