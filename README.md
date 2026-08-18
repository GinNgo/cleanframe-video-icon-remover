# CleanFrame

CleanFrame is a local web tool for removing a static icon from video that you own or have explicit permission to edit. It preserves frame dimensions, frame rate, duration, and audio; the video stream is necessarily re-encoded, so exact file size is not guaranteed.

## Rights and permitted use

Do not use this tool to remove a third-party owner watermark, hide provenance, evade Content ID, or edit media without permission. Every processing request requires a rights attestation and writes a local checksum audit record to `data/audit.jsonl`.

## Run on Windows

Requirements: Python 3.12+ and FFmpeg/ffprobe on `PATH`.

```powershell
python -m pip install -r requirements.txt
.\run.ps1
```

Open `http://127.0.0.1:8765`, choose a video, drag a rectangle around the static icon, select the closest logo shape, confirm your rights, and process the file. Diamond mode is tuned for Gemini-style sparkle icons and avoids changing the corners of the selected rectangle.

## Verify

```powershell
python -m unittest discover -s tests -v
```

For a processed file, compare source and output metadata:

```powershell
ffprobe -v error -show_streams -show_format -of json input.mp4
ffprobe -v error -show_streams -show_format -of json output.mp4
```

## Known limits

- Version 1 handles icons that stay in one position for the full clip.
- Shape-aware inpainting estimates pixels from the mask boundary; results depend on background motion, logo size, and selection accuracy.
- Output byte size can vary because modified video frames must be encoded again.
