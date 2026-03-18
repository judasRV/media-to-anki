# Media to Anki

A simple desktop tool to create Anki cards with audio (and optional images) from video/audio files and subtitles.

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

```
pip install -r requirements.txt
```

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
* Deck name is derived from the exported file name

## Future improvements

* Card preview/edit window
* Duplicate detection
* Batch generation from subtitles
* Tagging per source file

## License

MIT
